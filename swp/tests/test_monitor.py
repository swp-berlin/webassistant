import datetime
from unittest import mock

from django import test
from django.core import mail
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
ER  - \nTY  - ICOMM
TI  - Impact of COVID-19 lockdowns on individual mobility and the importance of socioeconomic factors
PY  - 2020-11
UR  - https://piie.com/publications/policy-briefs/impact-covid-19-lockdowns-individual-mobility-and-importance
L1  - https://www.piie.com/system/files/documents/pb20-14.pdf
SP  - 22
AU  - A. L. Phabet
AU  - Dr. Dyslexia
ER  - \n"""


class MonitorTestCase(test.TestCase):
    model = Monitor

    @classmethod
    def setUpTestData(cls):
        cls.now = now = timezone.localtime()

        cls.monitor = Monitor.objects.create(
            name='PIIE Monitor',
            recipients=['test-1@localhost', 'test-2@localhost'],
            is_active=True,
            created=now,
        )

        cls.thinktanks = Thinktank.objects.bulk_create([
            Thinktank(
                name='PIIE',
                url='https://www.piie.com/',
                unique_field='url',
                is_active=True,
                created=now,
            ),
            Thinktank(
                name='Deactivated Thinktank',
                url='https://example.net/',
                unique_field='url',
                created=now,
            ),
        ])

        cls.publications = Publication.objects.bulk_create([
            Publication(
                thinktank=cls.thinktanks[0],
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
                thinktank=cls.thinktanks[0],
                title='Already accessed publication',
                publication_date='2021',
                url='https://example.org',
                last_access=now - ONE_HOUR,
                created=now,
            ),
        ])

        cls.scrapers = Scraper.objects.bulk_create([
            Scraper(
                type=ScraperType.LIST_WITH_LINK_AND_DOC.value,
                thinktank=cls.thinktanks[0],
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
            self.assertEqual(monitor.next_run, monitor.annotated_next_run)

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

    def test_generate_ris_file(self):
        file = self.monitor.generate_ris_file(exclude_sent=True)
        self.assertEqual(file.name, 'PIIE Monitor.ris')
        data = file.file.getvalue()
        self.assertEqual(data, FULL_RIS_DATA)

    def test_send_monitor_publications(self):
        count = send_monitor_publications(self.monitor, now=self.now)
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(count, 2)

        self.assertEqual(mail.outbox[0].to, ['test-1@localhost'])
        self.assertTrue('PIIE Monitor' in mail.outbox[0].subject)

        attachments = mail.outbox[0].attachments
        self.assertEqual(len(attachments), 1)
        self.assertEqual(attachments[0][0], 'PIIE Monitor.ris')
        self.assertEqual(attachments[0][1], FULL_RIS_DATA)
        self.assertEqual(attachments[0][2], 'application/x-research-info-systems')

    def test_send_only_new_monitor_publications(self):
        self.model.objects.filter(pk=self.monitor.pk).update(last_sent=self.now)
        monitor = self.model.objects.get(pk=self.monitor.pk)

        count = send_monitor_publications(monitor, now=self.now)
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(count, 2)

        self.assertEqual(mail.outbox[0].attachments[0][1], NEW_RIS_DATA)
        self.assertEqual(mail.outbox[1].attachments[0][1], NEW_RIS_DATA)

    def test_new_monitor_publications(self):
        count = monitor_new_publications(self.monitor.pk, now=self.now)

        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(count, 2)

    def test_do_not_send_deactivated_monitor_publications(self):
        self.model.objects.filter(pk=self.monitor.pk).update(is_active=False)

        count = monitor_new_publications(self.monitor.pk, now=self.now)

        self.assertEqual(len(mail.outbox), 0)
        self.assertFalse(count)

    def test_do_not_send_empty_monitor_publications(self):
        Publication.objects.update(thinktank_id=self.thinktanks[1].pk)

        count = monitor_new_publications(self.monitor.pk, now=self.now)

        self.assertEqual(len(mail.outbox), 0)
        self.assertFalse(count)

    def test_do_not_send_outdated_monitor_publications(self):
        self.model.objects.filter(pk=self.monitor.pk).update(last_sent=self.now)

        count = monitor_new_publications(self.monitor.pk, now=self.now)

        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(count, 2)

        self.assertEqual(mail.outbox[0].attachments[0][1], NEW_RIS_DATA)
        self.assertEqual(mail.outbox[1].attachments[0][1], NEW_RIS_DATA)

    def test_do_not_dispatch_deactivated_monitor_publications(self):
        self.model.objects.filter(pk=self.monitor.pk).update(is_active=False)

        count = monitor_new_publications(self.monitor.pk)

        self.assertEqual(len(mail.outbox), 0)
        self.assertFalse(count)

    def test_do_not_dispatch_outdated_monitor_publications(self):
        Publication.objects.update(last_access=self.now - ONE_HOUR)
        self.model.objects.filter(pk=self.monitor.pk).update(last_sent=self.now)

        count = monitor_new_publications(self.monitor.pk)

        self.assertEqual(len(mail.outbox), 0)
        self.assertFalse(count)

    def test_schedule_monitors(self):
        with mock.patch(
            'swp.tasks.monitor.monitor_new_publications.apply_async',
            side_effect=lambda args, **kwargs: monitor_new_publications(*args)
        ) as dispatch_task:
            count = schedule_monitors(now=self.now)

            self.assertEqual(count, 1)
            self.assertTrue(dispatch_task.called)
