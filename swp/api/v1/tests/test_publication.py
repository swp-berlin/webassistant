from django import test
from django.urls import reverse
from django.utils import timezone
from cosmogo.utils.testing import create_user, login, request

from swp.models import Publication, Thinktank


class PublicationTestCase(test.TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.now = now = timezone.localtime()
        cls.user = create_user('test@localhost')

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
                is_active=True,
            ),
        ])
        cls.thinktank = cls.thinktanks[1]

        cls.publications = Publication.objects.bulk_create([
            Publication(
                thinktank=cls.thinktanks[0],
                title='Impact of COVID-19 lockdowns on individual mobility and the importance of socioeconomic factors',
                publication_date='2020-11',
                url='https://piie.com/publications/policy-briefs/impact-covid-19-lockdowns-individual-mobility-and-importance',
                pdf_url='https://www.piie.com/system/files/documents/pb20-14.pdf',
                pdf_pages=22,
            ),
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

    def test_list_filter(self):
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

        thinktank = response.data['thinktank']
        self.assertEqual(thinktank['id'], self.publication.thinktank_id)
        self.assertEqual(thinktank['name'], self.publication.thinktank.name)
