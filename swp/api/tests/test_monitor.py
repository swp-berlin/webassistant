from unittest import mock

from django import test
from django.utils import timezone
from cosmogo.utils.testing import create_user, login, request

from swp.models import Monitor, Thinktank, ThinktankFilter


class MonitorViewSetTestCase(test.TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.now = now = timezone.localtime()
        cls.user = create_user('test-user@localhost')

        cls.monitors = Monitor.objects.bulk_create([
            Monitor(name='Monitor A', recipients=['a.nobody@localhost', 'z.nobody@localhost'], created=now),
            Monitor(name='Monitor B', recipients=['b.nobody@localhost'], created=now),
            Monitor(name='Monitor C', recipients=['c.nobody@localhost'], created=now),
        ])
        cls.monitor = cls.monitors[0]

        cls.thinktanks = Thinktank.objects.bulk_create([
            Thinktank(
                name='PIIE',
                url='https://www.piie.com/',
                unique_fields=['url'],
                created=now,
                is_active=True,
            ),
            Thinktank(
                name='China Development Institute',
                url='http://en.cdi.org.cn/',
                unique_fields=['url'],
                created=now,
            ),
        ])

        cls.thinktank_filters = ThinktankFilter.objects.bulk_create([
            ThinktankFilter(monitor=cls.monitors[0], thinktank=cls.thinktanks[0]),
            ThinktankFilter(monitor=cls.monitors[0], thinktank=cls.thinktanks[0]),
        ])

    def setUp(self):
        login(self)

    def test_detail(self):
        with mock.patch('swp.tasks.update_publication_count.delay') as delay:
            response = request(self, '1:monitor-detail', args=[self.monitor.pk])

        self.assertTrue(delay.called)
        self.assertEqual(response.data['name'], self.monitor.name)
        self.assertEqual(response.data['description'], self.monitor.description)
        self.assertEqual(response.data['last_sent'], self.monitor.last_sent)
        self.assertEqual(response.data['interval'], self.monitor.interval)
        self.assertEqual(response.data['recipient_count'], self.monitor.recipient_count)
        self.assertEqual(response.data['publication_count'], self.monitor.publication_count)
        self.assertEqual(response.data['new_publication_count'], self.monitor.new_publication_count)
        self.assertEqual(response.data['recipients'], self.monitor.recipients)
        self.assertEqual(len(response.data['filters']), self.monitor.thinktank_filters.count())

    def test_list(self):
        with mock.patch('celery.canvas.group.delay') as delay:
            response = request(self, '1:monitor-list')

        self.assertTrue(delay.called)
        self.assertEqual(len(response.data), len(self.monitors))
