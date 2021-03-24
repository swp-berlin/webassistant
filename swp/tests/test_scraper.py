from unittest import mock

from django import test
from django.core import mail
from django.utils import timezone

from cosmogo.utils.testing import create_user

from swp.forms.publication import ScrapedPublicationForm
from swp.models import ErrorLevel, Publication, Scraper, ScraperError, Thinktank
from swp.tasks.scheduling import send_scraper_errors
from swp.utils.auth import get_user_queryset, get_superuser_email_addresses, get_error_recipient_email_addresses
from swp.utils.scraping.scraper import Scraper as _Scraper


class ScraperTestCase(test.TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.now = now = timezone.localtime()
        cls.user = create_user('user', is_error_recipient=True)
        cls.superuser_1 = create_user('superuser-1', is_superuser=True, is_error_recipient=True)
        cls.superuser_2 = create_user('superuser-2', is_superuser=True)
        cls.inactive_superuser = create_user('inactive-superuser', is_superuser=True, is_active=False, is_error_recipient=True)

        cls.thinktank = Thinktank.objects.create(
            name='PIIE',
            url='https://example.org',
            unique_fields=['url'],
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

    def test_error_recipient_email_addresses(self):
        emails = get_error_recipient_email_addresses()
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

    def test_form_normalization(self):
        fields = {
            'url': 'https://example.org',
            'title': 'A title' * 1000,
            'subtitle': 'Subtitle ' * 1000,
            'authors': [
                'A. Author ' * 1000,
            ],
        }

        form = ScrapedPublicationForm(data=fields, now=self.now)
        self.assertTrue(form.is_valid())

        instance = form.save(commit=False)
        self.assertLessEqual(len(instance.title), 1024)
        self.assertLessEqual(len(instance.subtitle), 1024)
        self.assertLessEqual(len(instance.authors[0]), 1024)

    def test_form_validation_missing_url(self):
        fields = {
            'title': 'A title',
        }

        form = ScrapedPublicationForm(data=fields, now=self.now)
        self.assertFalse(form.is_valid())

    def test_form_validation_missing_title(self):
        fields = {
            'url': 'https://example.org',
        }

        form = ScrapedPublicationForm(data=fields, now=self.now)
        self.assertFalse(form.is_valid())

    def test_form_save_minimal(self):
        fields = {
            'url': 'https://example.org',
            'title': 'A title',
        }

        form = ScrapedPublicationForm(data=fields, now=self.now)
        self.assertTrue(form.is_valid())

        instance = form.save(thinktank=self.thinktank)
        self.assertTrue(instance.pk)
        self.assertEqual(instance.ris_type, 'ICOMM')
        self.assertEqual(instance.thinktank, self.thinktank)
        self.assertEqual(instance.created, instance.last_access)
        self.assertEqual(instance.authors, [])

        self.assertEqual(Publication.objects.count(), 1)

    def test_form_save_with_pdf(self):
        fields = {
            'url': 'https://www.piie.com/publications/policy-briefs/uncertain-prospects-sovereign-wealth-funds-gulf-countries',
            'abstract': 'Among the best-known sovereign wealth funds (SWFs)—government-owned or controlled investment vehicles—are those funded by hydrocarbon revenues in the member economies of the Gulf Cooperation Council (GCC), which comprises all the Arab countries in the Persian Gulf except Iraq, namely Bahrain, Kuwait, Oman, Qatar, Saudi Arabia, and the United Arab Emirates. This Policy Brief comparesthe GCC SWFs with each other and with other funds in terms of their transparency and accountability onthe fifth SWF scoreboard, available here. Several factors, including the decline in oil prices in recent years, have slowed the growth of the GCC’s SWFs. This slower growth could further diminish their governance and transparency standards, which are already weaker than those of other SWFs. Efforts to improve their governance and accountability will be important to garner public support for these SWFs.\n',
            'title': 'Uncertain prospects for sovereign wealth funds of Gulf countries',
            'authors': [
                'Patrick Honohan (PIIE)',
            ],
            'pdf_url': 'https://www.piie.com/sites/default/files/documents/pb21-4.pdf',
            'pdf_pages': 14,
        }

        form = ScrapedPublicationForm(data=fields, now=self.now)
        self.assertTrue(form.is_valid())

        instance = form.save(commit=False, thinktank=self.thinktank)
        self.assertEqual(instance.ris_type, 'UNPB')
        self.assertEqual(instance.pdf_url, 'https://www.piie.com/sites/default/files/documents/pb21-4.pdf')
        self.assertEqual(instance.pdf_pages, 14)

    def test_scraper_scrape(self):
        result = {
            'fields': {
                'url': 'https://www.piie.com/publications/policy-briefs/uncertain-prospects-sovereign-wealth-funds-gulf-countries',
                'abstract': 'Among the best-known sovereign wealth funds (SWFs)—government-owned or controlled investment vehicles—are those funded by hydrocarbon revenues in the member economies of the Gulf Cooperation Council (GCC), which comprises all the Arab countries in the Persian Gulf except Iraq, namely Bahrain, Kuwait, Oman, Qatar, Saudi Arabia, and the United Arab Emirates. This Policy Brief compares the GCC SWFs with each other and with other funds in terms of their transparency and accountability on the fifth SWF scoreboard, available here. Several factors, including the decline in oil prices in recent years, have slowed the growth of the GCC’s SWFs. This slower growth could further diminish their governance and transparency standards, which are already weaker than those of other SWFs. Efforts to improve their governance and accountability will be important to garner public support for these SWFs.\n',
                'title': 'Uncertain prospects for sovereign wealth funds of Gulf countries',
                'pdf_url': 'https://www.piie.com/sites/default/files/documents/pb21-4.pdf',
                'pdf_pages': 14,
                'authors': [
                    'Julien Maire (former PIIE), Adnan Mazarei (PIIE) and Edwin M. Truman (PIIE)\n',
                ],
            },
            'errors': {
                'subtitle': {
                    'message': 'Zeitüberschreitung beim Iterieren der .field--no-subtitle Elemente',
                    'level': 'warning',
                }
            }
        }

        async def agen(*args):
            yield result

        with mock.patch.object(_Scraper, 'scrape') as scrape_mock:
            scrape_mock.side_effect = agen

            self.scraper.errors.all().delete()
            self.assertEqual(self.scraper.scraped_publications.count(), 0)

            self.scraper.scrape()
            self.assertTrue(scrape_mock.called)

            self.assertEqual(self.scraper.errors.filter(level=ErrorLevel.WARNING).count(), 1)
            self.assertEqual(self.scraper.scraped_publications.count(), 1)

    def test_incomplete_scrape(self):
        result = {
            'fields': {},
            'errors': {},
        }

        async def agen(*args):
            yield result

        with mock.patch.object(_Scraper, 'scrape', agen):
            self.scraper.errors.all().delete()

            self.scraper.scrape()

            self.assertEqual(self.scraper.error_count, 1)
            self.assertEqual(self.scraper.scraped_publications.count(), 0)

            error = self.scraper.errors.error_only().first()
            self.assertEqual(error.code, 'missing')
