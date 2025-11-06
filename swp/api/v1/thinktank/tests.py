from rest_framework.test import APITestCase

from swp.utils.testing import create_user, create_thinktank, create_scraper, login, request


class ThinktankTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = create_user('tester', is_superuser=True)
        cls.thinktank = thinktank = create_thinktank('Test')
        cls.scraper = create_scraper(thinktank)

    def setUp(self):
        login(self)

    def test_delete_active_thinktank(self):
        self.scraper.delete()
        self.thinktank.activate(self.user)

        request(self, '1:thinktank-detail', args=[self.thinktank.id], method='DELETE', status_code=400)

    def test_delete_referenced_thinktank(self):
        self.thinktank.deactivate(self.user)

        request(self, '1:thinktank-detail', args=[self.thinktank.id], method='DELETE', status_code=400)
