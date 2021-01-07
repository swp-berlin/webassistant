from typing import List, Mapping, Optional
from django import test
from django.urls import reverse
from django.utils import timezone

from cosmogo.utils.testing import login, request

from swp.models import Publication, Scraper, ScraperType, Thinktank, User


FIELDS = (
    'id',
    'name',
    'url',
    'is_active',
    'last_run',
    'publication_count',
    'scraper_count',
    'last_error_count',
)


def find_by_id(data: List[Mapping], value: int, *, key: str = 'id') -> Optional[int]:
    return [i for i, item in enumerate(data) if item[key] == value][0]


class ThinktankTestCase(test.TestCase):
    fixtures = ['groups', 'test-users']

    @classmethod
    def setUpTestData(cls):
        cls.now = now = timezone.localtime()
        cls.user = User.objects.get_by_natural_key('admin@localhost')

        cls.thinktanks = Thinktank.objects.bulk_create([
            Thinktank(
                name='PIIE',
                url='https://www.piie.com/',
                unique_field='T1-AB',
                created=now,
            ),
            Thinktank(
                name='China Development Institute',
                url='http://en.cdi.org.cn/',
                unique_field='url',
                created=now,
                is_active=False,
            ),
        ])

        cls.thinktank: Thinktank = cls.thinktanks[0]
        cls.deactivated_thinktank: Thinktank = cls.thinktanks[1]

        cls.scrapers = Scraper.objects.bulk_create([
            Scraper(
                type=ScraperType.LIST_WITH_DOCS.value,
                thinktank=cls.thinktank,
                data={'scraped': True},
                start_url='https://www.piie.com/research/publications/policy-briefs',
                checksum='de9474fa85634623fd9ae9838f949a02c9365ede3499a26c9be52363a8b7f214',
                created=now,
                last_run=now,
            ),
            Scraper(
                type=ScraperType.LIST_WITH_DOCS.value,
                thinktank=cls.deactivated_thinktank,
                data={'reported': True},
                start_url='https://en.cdi.org.cn/publications/annual-report',
                checksum='EN-CDI-ORG-CN',
                created=now,
            ),
            Scraper(
                type=ScraperType.LIST_WITH_DOCS.value,
                thinktank=cls.deactivated_thinktank,
                data={'staffed': True},
                start_url='https://en.cdi.org.cn/chief-of-staff',
                checksum='EN-CDI-ORG-CN-STAFF',
                created=now,
            ),
        ])

        cls.scraper: Scraper = cls.scrapers[0]
        cls.scraper.errors.create(code='E-0001', message='Test Error')
        cls.scraper.errors.create(code='E-0002', message='Test Error')

        cls.publications = Publication.objects.bulk_create([
            Publication(
                thinktank=cls.thinktanks[1],
                title='Annual Report 2019',
                publication_date='2019-04-17',
                url='http://en.cdi.org.cn/index.php?option=com_k2&view=item&layout=item&id=707',
                pdf_url='http://en.cdi.org.cn/publications/annual-report/annual-report-2019/download',
                pdf_pages=136,
            ),
            Publication(
                thinktank=cls.thinktanks[1],
                title='Annual Report 2018',
                publication_date='2020-05-19',
                url='http://en.cdi.org.cn/index.php?option=com_k2&view=item&layout=item&id=529',
                pdf_url='http://en.cdi.org.cn/publications/annual-report/annual-report-2018/download',
                pdf_pages=148,
            ),
        ])

        cls.publications[0].scrapers.set([cls.scrapers[1]])
        cls.publications[1].scrapers.set([cls.scrapers[1]])

        cls.list_url = reverse('1:thinktank-list')

    def setUp(self):
        login(self)

    def get_result(self, data: List[Mapping], id: int = None) -> Thinktank:
        return data[find_by_id(data, id or self.thinktank.pk)]

    def test_list(self):
        response = request(self, '1:thinktank-list')
        self.assertEqual(len(response.data), 2)

        item: Mapping = self.get_result(response.data)
        for field in FIELDS:
            self.assertEqual(item[field], getattr(self.thinktank, field), f'Field {field} mismatch')

    def test_active_list(self):
        response = request(self, f'{self.list_url}?is_active=true')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.thinktank.pk)

    def test_inactive_list(self):
        response = request(self, f'{self.list_url}?is_active=false')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.deactivated_thinktank.pk)

    def test_publication_count(self):
        response = request(self, '1:thinktank-list')

        item: Mapping = self.get_result(response.data, self.thinktank.pk)
        self.assertEqual(item['publication_count'], 0)
        self.assertEqual(self.thinktank.publication_count, 0)

        deactivated_item = self.get_result(response.data, self.deactivated_thinktank.pk)
        self.assertEqual(deactivated_item['publication_count'], 2)
        self.assertEqual(self.deactivated_thinktank.publication_count, 2)

    def test_scraper_count(self):
        response = request(self, '1:thinktank-list')

        item: Mapping = self.get_result(response.data, self.thinktank.pk)
        self.assertEqual(item['scraper_count'], 1)
        self.assertEqual(self.thinktank.scraper_count, 1)

        deactivated_item = self.get_result(response.data, self.deactivated_thinktank.pk)
        self.assertEqual(deactivated_item['scraper_count'], 2)
        self.assertEqual(self.deactivated_thinktank.scraper_count, 2)

    def test_last_error_count(self):
        response = request(self, '1:thinktank-list')

        item = self.get_result(response.data, self.thinktank.pk)
        self.assertEqual(item['last_error_count'], 2)
        self.assertEqual(self.thinktank.last_error_count, 2)
