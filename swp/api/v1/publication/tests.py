from rest_framework.test import APITestCase

from swp.utils.testing import create_publication, create_thinktank, create_user, login, request, add_to_group

from .serializers import PublicationSearchSerializer


class PublicationTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = create_user('tester', is_superuser=True)
        cls.thinktank = thinktank = create_thinktank('Test')
        cls.publication = create_publication(thinktank, 'Test')

    def setUp(self):
        login(self)

    def test_delete(self):
        request(self, '1:publication-detail', args=[self.publication.id], method='DELETE', status_code=204)

    def test_search(self):
        request(self, '1:publication-search', method='POST', data={})

    def test_search_as_researcher(self):
        researcher = create_user('researcher')

        add_to_group(researcher, 'swp-researcher')
        login(self, researcher)
        request(self, '1:publication-search', method='POST', data={})

    def test_search_serializer(self):
        serializer = PublicationSearchSerializer(instance=None)

        self.assertFalse(serializer.data)

    def test_search_invalid(self):
        request(self, '1:publication-search', status_code=400, method='POST', data={'test': 1})
