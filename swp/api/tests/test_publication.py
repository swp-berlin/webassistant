import datetime

from contextlib import contextmanager
from unittest.mock import patch
from urllib.parse import urlencode

from django import test
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

from swp.api.viewsets.publication import get_query_vector
from swp.models import Publication, Monitor
from swp.utils.requests import TimeOutSession
from swp.utils.testing import (
    login,
    request,
    clear_cache,
    create_user,
    add_to_group,
    create_monitor,
    create_thinktank,
    get_random_embedding_vector,
)

ONE_HOUR = datetime.timedelta(hours=1)


@contextmanager
def patch_monitor_query(*publications):
    if publications:
        return_value = models.Q(id__in=[publication.id for publication in publications])
    else:
        return_value = models.Q(id=None)

    with patch.object(Monitor, 'get_query', return_value=return_value) as get_query:
        yield get_query


class PublicationTestCase(test.TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.now = now = timezone.localtime()
        cls.today = today = timezone.localdate(now)
        cls.user = user = create_user('test@localhost')

        add_to_group(user, 'swp-researcher')

        cls.thinktanks = thinktanks = [
            create_thinktank(
                name='PIIE',
                url='https://www.piie.com/',
                unique_fields=['T1-AB'],
                created=now,
            ),
            create_thinktank(
                name='China Development Institute',
                url='http://en.cdi.org.cn/',
                unique_fields=['url'],
                created=now,
                is_active=True,
            ),
        ]

        cls.thinktank = thinktanks[1]

        [thinktank_0, thinktank_1] = thinktanks

        cls.monitors = [
            create_monitor(
                name='Monitor A',
                recipients=['nobody@localhost'],
                created=now,
                query=f'thinktank.id:{thinktank_0.id} AND title:("COVID-19" OR "COVID-20")',
            ),
            create_monitor(
                name='Monitor B',
                recipients=['nobody@localhost'],
                created=now,
                last_sent=now,
                query=f'thinktank.id:{thinktank_1.id} AND title:"Annual Report"',
            ),
            create_monitor(
                name='Monitor C',
                recipients=['nobody@localhost'],
                created=now,
            ),
        ]

        cls.publications = Publication.objects.bulk_create([
            Publication(
                thinktank=cls.thinktanks[0],
                title='Impact of COVID-19 lockdowns on individual mobility and the importance of socioeconomic factors',
                publication_date='2020-11',
                publication_date_clean=today,
                url='https://piie.com/publications/policy-briefs/impact-covid-19-lockdowns-individual-mobility-and-importance',
                pdf_url='https://www.piie.com/system/files/documents/pb20-14.pdf',
                pdf_pages=22,
                last_access=now,
                created=now,
            ),
            Publication(
                thinktank=cls.thinktanks[1],
                title='Annual Report 2019',
                publication_date='2019-04-17',
                publication_date_clean=today,
                url='http://en.cdi.org.cn/index.php?option=com_k2&view=item&layout=item&id=707',
                pdf_url='http://en.cdi.org.cn/publications/annual-report/annual-report-2019/download',
                pdf_pages=136,
                last_access=now - ONE_HOUR,
                created=now,
            ),
            Publication(
                thinktank=cls.thinktanks[1],
                title='Annual Report 2018',
                publication_date='2020-05-19',
                publication_date_clean=today,
                url='http://en.cdi.org.cn/index.php?option=com_k2&view=item&layout=item&id=529',
                pdf_url='http://en.cdi.org.cn/publications/annual-report/annual-report-2018/download',
                pdf_pages=148,
                last_access=now,
                created=now,
            ),
        ])
        cls.publication = cls.publications[1]

        cls.list_url = reverse('1:publication-list')

    def setUp(self):
        login(self)

    def test_list(self):
        response = request(self, '1:publication-list')
        self.assertEqual(response.data['count'], 3)
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(len(response.data['results']), 3)

    def test_thinktank_filter(self):
        response = request(self, f'{self.list_url}?thinktank_id={self.thinktank.pk}')
        self.assertEqual(response.data['count'], 2)

    def test_detail(self):
        response = request(self, '1:publication-detail', args=[self.publication.pk])
        self.assertEqual(response.data['title'], self.publication.title)
        self.assertEqual(response.data['authors'], self.publication.authors)
        self.assertEqual(response.data['publication_date'], self.publication.publication_date)
        self.assertEqual(response.data['abstract'], self.publication.abstract)
        self.assertEqual(response.data['pdf_url'], self.publication.pdf_url)
        self.assertEqual(response.data['pdf_pages'], self.publication.pdf_pages)

    def test_monitor_empty_filter(self):
        with patch_monitor_query():
            response = request(self, f'{self.list_url}?monitor={self.monitors[0].pk}')

        self.assertEqual(response.data['count'], 0)

    def test_monitor_filter(self):
        with patch_monitor_query(self.publications[1], self.publications[2]):
            response = request(self, f'{self.list_url}?monitor={self.monitors[1].pk}')

        self.assertEqual(response.data['count'], 2)

    def test_monitor_active_filter(self):
        monitor = self.monitors[1]

        with patch_monitor_query(self.publications[1], self.publications[2]):
            response = request(self, f'{self.list_url}?monitor={monitor.pk}&is_active=true')
            self.assertEqual(response.data['count'], 2)

            monitor.update_publication_count()
            self.assertEqual(monitor.publication_count, 2)

    def test_monitor_inactive_filter(self):
        with patch_monitor_query(self.publications[1], self.publications[2]):
            response = request(self, f'{self.list_url}?monitor={self.monitors[1].pk}&is_active=false')

        self.assertEqual(response.data['count'], 0)

    def test_monitor_active_since_filter(self):
        query_string = urlencode({
            'monitor': self.monitors[1].pk,
            'is_active': True,
            'since': self.monitors[1].last_sent,
        })

        with patch_monitor_query(self.publications[1], self.publications[2]):
            response = request(self, f'{self.list_url}?{query_string}')

        self.assertEqual(response.data['count'], 1)

    def test_monitor_active_outdated_filter(self):
        query_string = urlencode({
            'monitor': self.monitors[1].pk,
            'is_active': True,
            'since': self.now + ONE_HOUR,
        })

        with patch_monitor_query(self.publications[1], self.publications[2]):
            response = request(self, f'{self.list_url}?{query_string}')

        self.assertEqual(response.data['count'], 0)

    def test_research(self):
        url = reverse('1:publication-research')
        params = urlencode({'query': 'COVID-19'})

        request(self, f'{url}?{params}')

    def test_research_as_editor(self):
        add_to_group(self.user, 'swp-editor')
        PublicationTestCase.test_research(self)

    def test_research_invalid_query(self):
        url = reverse('1:publication-research')
        params = urlencode({'query': 'thinktank.id:'})

        request(self, f'{url}?{params}', status_code=400)

    @clear_cache(get_query_vector)
    def helper_research_full_text(self, success, result, status_code):
        url = reverse('1:publication-research')
        params = urlencode({'query': '<COVID-19>'})
        return_value = success, result

        with patch.object(TimeOutSession, 'json', return_value=return_value) as json:
            request(self, f'{url}?{params}', status_code=status_code)

        self.assertTrue(json.called)

    def test_research_full_text_success(self):
        vector = get_random_embedding_vector(settings.EMBEDDING_VECTOR_DIMS)

        self.helper_research_full_text(True, vector, 200)

    def test_research_full_text_unavailable(self):
        self.helper_research_full_text(None, Exception('unavailable'), 503)

    def test_research_full_text_invalid(self):
        self.helper_research_full_text(False, 'invalid', 400)

    def test_ris(self):
        url = reverse('1:publication-ris')
        params = urlencode({
            'query': 'COVID-19',
            'pool': 0,
            'start_date': self.now.strftime('%Y-%m-%d'),
            'end_date': self.now.strftime('%Y-%m-%d'),
        })

        request(self, f'{url}?{params}')
