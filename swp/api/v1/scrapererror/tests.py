from django.test import TestCase

from swp.utils.testing import create_user, create_thinktank, create_scraper, create_scraper_error, login, request


class ScraperErrorTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = create_user('tester', is_superuser=True)
        cls.thinktank = thinktank = create_thinktank('Test')
        cls.scraper = scraper = create_scraper(thinktank)
        cls.scraper_error = create_scraper_error(scraper)

    def setUp(self):
        login(self)

    def test_delete(self):
        request(self, '1:scraper-error-detail', args=[self.scraper_error.id], status_code=204, method='DELETE')
