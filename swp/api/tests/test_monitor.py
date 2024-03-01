from unittest import mock

from django import test
from django.utils import timezone

from swp.utils.testing import create_user, login, request, create_monitor, create_thinktank, add_to_group


class MonitorViewSetTestCase(test.TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.now = now = timezone.localtime()
        cls.user = user = create_user('test-user@localhost')

        add_to_group(user, 'swp-editor')

        cls.monitors = [
            create_monitor(name='Monitor A', recipients=['a.nobody@localhost', 'z.nobody@localhost'], created=now),
            create_monitor(name='Monitor B', recipients=['b.nobody@localhost'], created=now),
            create_monitor(name='Monitor C', recipients=['c.nobody@localhost'], created=now),
        ]
        cls.monitor = cls.monitors[0]

        cls.thinktanks = [
            create_thinktank(
                name='PIIE',
                url='https://www.piie.com/',
                unique_fields=['url'],
                created=now,
                is_active=True,
            ),
            create_thinktank(
                name='China Development Institute',
                url='http://en.cdi.org.cn/',
                unique_fields=['url'],
                created=now,
            ),
        ]

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

        self.assertNotIn('recipients', response.data)
        self.assertNotIn('zotero_keys', response.data)

    def test_list(self):
        with mock.patch('celery.canvas.group.delay') as delay:
            response = request(self, '1:monitor-list')

        self.assertTrue(delay.called)
        self.assertEqual(len(response.data), len(self.monitors))
