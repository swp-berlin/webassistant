from rest_framework.test import APITestCase

from swp.utils.testing import create_user, create_monitor, login, request


class MonitorTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = create_user('tester', is_superuser=True)
        cls.monitor = create_monitor()

    def setUp(self):
        login(self)

    def test_activate(self):
        self.monitor.set_active(False)
        request(self, '1:monitor-activate', args=[self.monitor.id], method='POST', data={})
        self.monitor.refresh_from_db(fields=['is_active'])
        self.assertTrue(self.monitor.is_active)

    def test_deactivate(self):
        self.monitor.set_active(True)
        request(self, '1:monitor-deactivate', args=[self.monitor.id], method='POST', data={})
        self.monitor.refresh_from_db(fields=['is_active'])
        self.assertFalse(self.monitor.is_active)
