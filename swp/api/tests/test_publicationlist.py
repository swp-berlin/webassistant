from django.test import TestCase

from swp.models import Thinktank, Publication, PublicationList
from swp.utils.ris import RIS_MEDIA_TYPE
from swp.utils.testing import create_user, request, login


class PublicationTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = user = create_user('publication-list')
        cls.thinktank = thinktank = Thinktank.objects.create(name='Test-Thinktank')
        cls.publication = publication = Publication.objects.create(thinktank=thinktank, title='Test-Publication')
        cls.publication_list = publication_list = PublicationList.objects.create(user=user, name='Test')
        cls.publication_list_entry = publication_list.entries.create(publication=publication)

    def setUp(self):
        login(self)

    def test_list_endpoint(self):
        response = request(self, 'api:publication-list-list')

        self.assertEqual(len(response.data), 1)

    def test_detail_endpoint(self):
        response = request(self, 'api:publication-list-detail', args=[self.publication_list.id])

        self.assertIn('publications', response.data)

    def test_create(self):
        request(self, 'api:publication-list-list', name='Test-Create', status_code=201)

        self.assertEqual(self.user.publication_lists.count(), 2)

    def test_add_endpoint(self):
        publication = Publication.objects.create(thinktank=self.thinktank, title='Test-Publication-Add')
        args = self.publication_list.id, publication.id

        request(self, 'api:publication-list-add', args=args, status_code=201)

        self.assertEqual(self.publication_list.entries.count(), 2)

    def test_remove_endpoint(self):
        args = self.publication_list.id, self.publication.id

        request(self, 'api:publication-list-remove', args=args, status_code=204)

        self.assertEqual(self.publication_list.entries.count(), 0)

    def test_export_endpoint(self):
        response = request(self, 'api:publication-list-export', args=[self.publication_list.id])

        self.assertEqual(response['Content-Type'], RIS_MEDIA_TYPE)
