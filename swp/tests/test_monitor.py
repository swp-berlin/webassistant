import datetime
from unittest import mock

from django import test
from django.core import mail
from django.core.exceptions import ValidationError
from django.utils import timezone

from swp.models import Monitor, Publication, Scraper, Thinktank
from swp.scraper.types import ScraperType
from swp.tasks.monitor import (
    monitor_new_publications,
    send_monitor_publications,
    schedule_monitors,
)

ONE_HOUR = datetime.timedelta(hours=1)
ONE_DAY = datetime.timedelta(days=1)


NEW_RIS_DATA = b"""TY  - ICOMM
TI  - Impact of COVID-19 lockdowns on individual mobility and the importance of socioeconomic factors
PY  - 2020-11
UR  - https://piie.com/publications/policy-briefs/impact-covid-19-lockdowns-individual-mobility-and-importance
L1  - https://www.piie.com/system/files/documents/pb20-14.pdf
SP  - 22
AU  - A. L. Phabet
AU  - Dr. Dyslexia
ER  - \n"""

FULL_RIS_DATA = b"""TY  - ICOMM
TI  - Already accessed publication
PY  - 2021
UR  - https://example.org
DO  - 10.1000/182
SN  - 978-3-16-148410-0
ER  - \nTY  - ICOMM
TI  - Impact of COVID-19 lockdowns on individual mobility and the importance of socioeconomic factors
PY  - 2020-11
UR  - https://piie.com/publications/policy-briefs/impact-covid-19-lockdowns-individual-mobility-and-importance
L1  - https://www.piie.com/system/files/documents/pb20-14.pdf
SP  - 22
AU  - A. L. Phabet
AU  - Dr. Dyslexia
ER  - \n"""


ZOTERO_COLLECTIONS = {'92BRC33T', 'BFGHEX22'}

# Random secret key for Zotero API access
ZOTERO_API_KEY = 'HM91didFKOzWFghIr8yfv6N5'
# Invalid combined Zotero key (for a group's collection)
BAD_ZOTERO_KEY = f'{ZOTERO_API_KEY}/groups/1234567/group-name/collections/CID6789V'


class MonitorTestCase(test.TestCase):
    model = Monitor

    @classmethod
    def setUpTestData(cls):
        cls.now = now = timezone.localtime()

        cls.monitor = Monitor.objects.create(
            name='PIIE Monitor',
            recipients=['test-1@localhost', 'test-2@localhost'],
            zotero_keys=[
                'W9IOwvQPucFnh9J0BmZFNv92/users/1111111/items',
                'W9IOwvQPucFnh9J0BmZFNv92/users/1111111/collections/92BRC33T/items',
                'W9IOwvQPucFnh9J0BmZFNv92/users/1111111/collections/BFGHEX22/items/',
            ],
            is_active=True,
            created=now,
        )

        cls.thinktanks = thinktanks = Thinktank.objects.bulk_create([
            Thinktank(
                name='PIIE',
                url='https://www.piie.com/',
                unique_fields=['url'],
                is_active=True,
                created=now,
            ),
            Thinktank(
                name='Deactivated Thinktank',
                url='https://example.net/',
                unique_fields=['url'],
                created=now,
            ),
        ])

        thinktank, *thinktanks = thinktanks

        cls.publications = Publication.objects.bulk_create([
            Publication(
                thinktank=thinktank,
                title='Impact of COVID-19 lockdowns on individual mobility and the importance of socioeconomic factors',
                authors=['A. L. Phabet', 'Dr. Dyslexia'],
                publication_date='2020-11',
                url='https://piie.com/publications/policy-briefs/impact-covid-19-lockdowns-individual-mobility-and-importance',
                pdf_url='https://www.piie.com/system/files/documents/pb20-14.pdf',
                pdf_pages=22,
                last_access=now,
                created=now,
            ),
            Publication(
                thinktank=thinktank,
                title='Already accessed publication',
                publication_date='2021',
                url='https://example.org',
                isbn='978-3-16-148410-0',
                doi='10.1000/182',
                last_access=now - ONE_HOUR,
                created=now,
            ),
        ])

        cls.scrapers = Scraper.objects.bulk_create([
            Scraper(
                type=ScraperType.LIST_WITH_LINK_AND_DOC.value,
                thinktank=thinktank,
                data={
                    "type": "List",
                    "selector": ".node--publication",
                    "paginator": {
                        "type": "Page",
                        "max_pages": 1,
                        "list_selector": ".view-content",
                        "button_selector": ".pager .pager-next a",
                    },
                    "resolvers": [
                        {
                            "key": "url",
                            "type": "Attribute",
                            "selector": ".field--title a", "attribute": "href",
                        },
                        {
                            "type": "Link",
                            "selector": ".field--title a",
                            "resolvers": [
                                {"key": "abstract", "type": "Static", "value": "Always the same abstract"},
                                {"key": "title", "type": "Data", "selector": ".field--title"},
                                {"key": "abstract", "type": "Data", "selector": ".field--body"},
                                {"key": "author", "type": "Data", "selector": ".field--contributor"},
                                {"key": "pdf_url", "type": "Document", "selector": ".field--view-full-document a"},
                            ],
                        },
                    ],
                },
                start_url='https://www.piie.com/research/publications/policy-briefs',
                checksum='de9474fa85634623fd9ae9838f949a02c9365ede3499a26c9be52363a8b7f214',
                created=now,
                last_run=now,
                is_active=True,
            ),
        ])

    def test_publications(self):
        self.assertSequenceEqual(self.monitor.publications.order_by('pk'), self.publications)

    def test_new_publications(self):
        self.model.objects.filter(pk=self.monitor.pk).update(last_sent=self.now)
        monitor = self.model.objects.get(pk=self.monitor.pk)

        new_publications = list(monitor.new_publications)
        self.assertEqual(len(new_publications), 1)
        self.assertEqual(new_publications[0].pk, self.publications[0].pk)

    def test_update_publication_count(self):
        monitor = self.model.objects.get(pk=self.monitor.pk)

        self.assertEqual(monitor.publication_count, 0)
        self.assertEqual(monitor.new_publication_count, 0)

        counts = monitor.update_publication_count()

        self.assertEqual(counts, (2, 2))
        self.assertEqual(monitor.publication_count, 2)
        self.assertEqual(len(monitor.publications), 2)
        self.assertEqual(monitor.new_publication_count, 2)
        self.assertEqual(len(monitor.new_publications), 2)

    def test_next_run(self):
        monitor = self.model.objects.annotate_next_run('annotated_next_run', now=self.now).get(pk=self.monitor.pk)
        with mock.patch('django.utils.timezone.localtime', return_value=self.now):
            self.assertEqual(monitor.annotated_next_run, self.now)
            self.assertEqual(monitor.next_run, self.now)

    def test_next_run_with_last_sent(self):
        self.model.objects.filter(pk=self.monitor.pk).update(last_sent=self.now)
        monitor = self.model.objects.annotate_next_run('annotated_next_run', now=self.now).get(pk=self.monitor.pk)

        self.assertEqual(monitor.annotated_next_run, self.now + ONE_DAY)
        self.assertEqual(monitor.next_run, self.now + ONE_DAY)

    def test_next_run_before(self):
        queryset = self.model.objects.next_run_before(self.now + ONE_HOUR, now=self.now)
        self.assertEqual(queryset.count(), 1)

        self.model.objects.filter(pk=self.monitor.pk).update(is_active=False)
        self.assertEqual(queryset.count(), 1)

    def test_next_run_before_with_last_sent(self):
        self.model.objects.filter(pk=self.monitor.pk).update(last_sent=self.now - ONE_HOUR)
        queryset = self.model.objects.next_run_before(self.now + ONE_DAY, now=self.now)

        self.assertEqual(queryset.count(), 1)

    def test_next_run_between(self):
        queryset = self.model.objects.next_run_between(self.now, self.now + ONE_HOUR + ONE_HOUR, now=self.now)
        self.assertEqual(queryset.count(), 1)

        self.model.objects.filter(pk=self.monitor.pk).update(is_active=False)
        self.assertEqual(queryset.count(), 1)

    def test_scheduled_during_next_hour(self):
        queryset = self.model.objects.scheduled_during_next_hour(self.now)
        self.assertEqual(queryset.count(), 1)

        self.model.objects.filter(pk=self.monitor.pk).update(is_active=False)
        self.assertEqual(queryset.count(), 0)

    def test_generate_ris_data(self):
        data = self.monitor.generate_ris_data()
        self.assertEqual(data, FULL_RIS_DATA)

    def test_generate_new_ris_data(self):
        self.model.objects.filter(pk=self.monitor.pk).update(last_sent=self.now)
        monitor = self.model.objects.get(pk=self.monitor.pk)

        data = monitor.generate_ris_data(exclude_sent=True)
        self.assertEqual(data, NEW_RIS_DATA)

    def test_do_not_generate_outdated_ris_data(self):
        Publication.objects.update(last_access=self.now - ONE_HOUR)
        self.model.objects.filter(pk=self.monitor.pk).update(last_sent=self.now)
        monitor = self.model.objects.get(pk=self.monitor.pk)

        data = monitor.generate_ris_data(exclude_sent=True)
        self.assertEqual(data, b'')

    def test_send_monitor_publications(self):
        with mock.patch('swp.tasks.monitor.post_zotero_publication.delay') as post_zotero_publication:
            count = send_monitor_publications(self.monitor, now=self.now)
            self.assertEqual(len(mail.outbox), 2)
            self.assertEqual(count, 2)

            call_args = post_zotero_publication.call_args[0]
            self.assertIsInstance(call_args[0], list)
            self.assertEqual(call_args[1], 'W9IOwvQPucFnh9J0BmZFNv92')
            self.assertEqual(call_args[2], '/users/1111111/items')

            api_item = call_args[0][1]
            self.assertIsInstance(api_item, dict)
            self.assertSetEqual(set(api_item['collections']), ZOTERO_COLLECTIONS)

            attachment_item = call_args[0][2]
            self.assertEqual(attachment_item['itemType'], 'attachment')
            self.assertEqual(attachment_item['parentItem'], api_item['key'])

        self.assertEqual(mail.outbox[0].to, ['test-1@localhost'])
        self.assertTrue('PIIE Monitor' in mail.outbox[0].subject)

        attachments = mail.outbox[0].attachments
        self.assertEqual(len(attachments), 1)
        self.assertEqual(attachments[0][0], 'PIIE Monitor.ris')
        self.assertEqual(attachments[0][1], FULL_RIS_DATA)
        self.assertEqual(attachments[0][2], 'application/x-research-info-systems')

        monitor = self.model.objects.get(pk=self.monitor.pk)
        self.assertEqual(monitor.last_sent, self.now)

    def test_send_only_new_monitor_publications(self):
        self.model.objects.filter(pk=self.monitor.pk).update(last_sent=self.now)
        monitor = self.model.objects.get(pk=self.monitor.pk)

        with mock.patch('swp.tasks.monitor.post_zotero_publication.apply_async'):
            count = send_monitor_publications(monitor, now=self.now)

        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(count, 2)
        self.assertEqual(monitor.last_sent, self.now)

        self.assertEqual(mail.outbox[0].attachments[0][1], NEW_RIS_DATA)
        self.assertEqual(mail.outbox[1].attachments[0][1], NEW_RIS_DATA)

    def test_new_monitor_publications(self):
        with mock.patch('swp.tasks.monitor.post_zotero_publication.apply_async'):
            count = monitor_new_publications(self.monitor.pk, now=self.now)

        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(count, 2)

        monitor = self.model.objects.get(pk=self.monitor.pk)
        self.assertEqual(monitor.last_sent, self.now)

    def test_only_new_monitor_publications(self):
        self.model.objects.filter(pk=self.monitor.pk).update(last_sent=self.now)

        with mock.patch('swp.tasks.monitor.post_zotero_publication.apply_async'):
            count = monitor_new_publications(self.monitor.pk, now=self.now)

        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(count, 2)

        self.assertEqual(mail.outbox[0].attachments[0][1], NEW_RIS_DATA)
        self.assertEqual(mail.outbox[1].attachments[0][1], NEW_RIS_DATA)

    def test_do_not_send_deactivated_monitor_publications(self):
        self.model.objects.filter(pk=self.monitor.pk).update(is_active=False)

        count = monitor_new_publications(self.monitor.pk, now=self.now)

        self.assertEqual(len(mail.outbox), 0)
        self.assertFalse(count)

        monitor = self.model.objects.get(pk=self.monitor.pk)
        self.assertIsNone(monitor.last_sent)

    def test_do_not_send_empty_monitor_publications(self):
        Publication.objects.update(thinktank_id=self.thinktanks[1].pk)

        count = monitor_new_publications(self.monitor.pk, now=self.now)

        self.assertEqual(len(mail.outbox), 0)
        self.assertFalse(count)

        monitor = self.model.objects.get(pk=self.monitor.pk)
        self.assertIsNone(monitor.last_sent)

    def test_do_not_send_outdated_monitor_publications(self):
        Publication.objects.update(last_access=self.now - ONE_HOUR)
        self.model.objects.filter(pk=self.monitor.pk).update(last_sent=self.now)

        count = monitor_new_publications(self.monitor.pk)

        self.assertEqual(len(mail.outbox), 0)
        self.assertFalse(count)

    def test_schedule_monitors(self):
        with mock.patch(
            'swp.tasks.monitor.monitor_new_publications.apply_async',
            side_effect=lambda args, kwargs, **options: monitor_new_publications(*args, **kwargs)
        ) as dispatch_task:
            with mock.patch('swp.tasks.monitor.post_zotero_publication.apply_async'):
                count = schedule_monitors(now=self.now)

            self.assertEqual(count, 1)
            self.assertTrue(dispatch_task.called)
            self.assertEqual(dispatch_task.call_count, 1)

            call_args = dispatch_task.call_args[1]
            self.assertEqual(call_args['eta'], self.now)

    def test_monitor_zotero_keys(self):
        self.assertTrue(self.monitor.is_zotero)

    def test_monitor_zotero_publication_keys(self):
        api_key, path, collections = self.monitor.get_zotero_publication_keys()[0]
        self.assertEqual(api_key, 'W9IOwvQPucFnh9J0BmZFNv92')
        self.assertEqual(path, '/users/1111111/items')
        self.assertSetEqual(set(collections), ZOTERO_COLLECTIONS)

    def test_invalid_monitor_publication_keys(self):
        self.model.objects.filter(pk=self.monitor.pk).update(zotero_keys=[BAD_ZOTERO_KEY])

        monitor = self.model.objects.get(pk=self.monitor.pk)

        with self.assertRaises(ValidationError):
            monitor.full_clean()

        with self.assertRaises(ValueError):
            monitor.get_zotero_publication_keys()

        with mock.patch('swp.models.monitor.capture_message') as capture_message:
            empty_keys = monitor.get_zotero_publication_keys(fail_silently=True)
            self.assertListEqual(empty_keys, [])
            self.assertTrue(capture_message.called)
