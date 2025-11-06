from rest_framework.test import APITestCase

from swp.models import PublicationList, PublicationListEntry, Publication
from swp.utils.testing import create_user, create_thinktank, create_publication, login, request


class PublicationListTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = user = create_user('tester', is_superuser=True)
        cls.thinktank = thinktank = create_thinktank('Test')
        cls.publication = publication = create_publication(thinktank, 'Test')
        cls.publication_list = publication_list = PublicationList.objects.create(user=user, name='Test')
        cls.publication_list_entry =  PublicationListEntry.objects.create(
            publication=publication,
            publication_list=publication_list,
        )

    def setUp(self):
        login(self)

    def test_list(self):
        user = create_user('another')

        PublicationList.objects.create(user=user, name='Another Test')

        response = request(self, '1:publication-list-list')

        self.assertEqual(response.data.get('count'), 1)

    def test_add(self):
        publication = create_publication(self.thinktank, 'Test 2')

        request(self, '1:publication-list-add', args=[self.publication_list.id], publication=publication.id)

    def test_add_already_an_entry(self):
        request(self, '1:publication-list-add', args=[self.publication_list.id], status_code=400, publication=self.publication.id)

    def test_remove(self):
        request(self, '1:publication-list-remove', args=[self.publication_list.id], publication=self.publication.id)

    def test_remove_not_an_entry(self):
        publication = create_publication(self.thinktank, 'Test 2')

        request(self, '1:publication-list-remove', args=[self.publication_list.id], status_code=400, publication=publication.id)
