from django import test
from django.core import mail
from django.utils import timezone
from cosmogo.utils.testing import create_user

from swp.models import Scraper, ScraperError, Thinktank, ErrorLevel
from swp.tasks.scheduling import send_scraper_errors
from swp.utils.auth import get_user_queryset, get_superuser_email_addresses


class ScraperTestCase(test.TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.now = now = timezone.localtime()
        cls.user = create_user('user')
        cls.superuser_1 = create_user('superuser-1', is_superuser=True)
        cls.superuser_2 = create_user('superuser-2', is_superuser=True)
        cls.inactive_superuser = create_user('inactive-superuser', is_superuser=True, is_active=False)

        cls.thinktank = Thinktank.objects.create(
            name='PIIE',
            url='https://example.org',
            unique_field='url',
            is_active=True,
            created=now,
        )

        cls.scraper = Scraper.objects.create(
            thinktank=cls.thinktank,
            start_url='https://www.piie.com/research/publications/policy-briefs',
            data={'mocked': True},
            created=now,
        )

        cls.scraper_errors = ScraperError.objects.bulk_create([
            ScraperError(
                scraper=cls.scraper,
                identifier='A Warning',
                message='Let this be a warning',
                level=ErrorLevel.WARNING,
                timestamp=now,
            ),
            ScraperError(
                scraper=cls.scraper,
                identifier='An Error',
                message='Let this be an error',
                level=ErrorLevel.ERROR,
                timestamp=now,
            ),
        ])

    def test_total_superuser_count(self):
        superusers = get_user_queryset(is_superuser=True)
        self.assertEqual(len(superusers), 3)

    def test_superuser_email_addresses(self):
        emails = get_superuser_email_addresses()
        self.assertEqual(len(emails), 2)

    def test_scraper_error_count(self):
        self.assertEqual(self.scraper.error_count, 1)

    def test_send_scraper_errors(self):
        count = send_scraper_errors(self.scraper)

        self.assertEqual(count, 2)
        self.assertEqual(len(mail.outbox), 2)

        self.assertEqual(mail.outbox[0].to, ['superuser-1@test.case'])
        self.assertIn(self.scraper.name, mail.outbox[0].subject)

    def test_do_not_send_errors_for_warnings(self):
        self.scraper.errors.all().update(level=ErrorLevel.WARNING)
        count = send_scraper_errors(self.scraper)

        self.assertFalse(count)
        self.assertEqual(len(mail.outbox), 0)

    def test_do_not_send_to_inactive_users(self):
        get_user_queryset().update(is_active=False)

        count = send_scraper_errors(self.scraper)

        self.assertFalse(count)
        self.assertEqual(len(mail.outbox), 0)
