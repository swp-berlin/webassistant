from django.test import TestCase
from django.utils.timezone import localtime

from swp.models import Pool, ScraperError
from swp.tasks import send_scraper_errors
from swp.utils.testing import create_user, create_thinktank, create_scraper, create_scraper_error


class ErrorReportTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = create_user('scraper', is_error_recipient=True)
        cls.thinktank = thinktank = create_thinktank()
        cls.scraper = scraper = create_scraper(thinktank)
        cls.error = create_scraper_error(scraper)

    def test_send_scraper_errors(self, using=None):
        count = send_scraper_errors(using=using)

        self.assertEqual(count, 1)

    def test_send_scraper_errors_to_user_with_pools(self, using=None):
        user = create_user('pool', is_error_recipient=True)
        pool = Pool.objects.create(name='pool')

        user.pools.add(pool)

        count = send_scraper_errors(using=using)

        self.assertEqual(count, 1)

    def test_send_scraper_errors_no_pools(self, using=None):
        ScraperError.objects.update(sent=localtime(None))

        count = send_scraper_errors(using=using)

        self.assertEqual(count, 0)
