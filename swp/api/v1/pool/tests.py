from rest_framework.test import APITestCase

from swp.utils.testing import create_user, login, request


class PoolTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = create_user('tester', is_superuser=True)

    def setUp(self):
        login(self)

    def test_update_pool(self):
        request(self, '1:pool-detail', args=[0], method='PATCH', data={'name': 'Updated'})
