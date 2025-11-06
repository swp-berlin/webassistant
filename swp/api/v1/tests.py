from django.utils.timezone import localtime

from rest_framework.test import APITestCase

from swp.models import AuthToken
from swp.utils.testing import create_user, request


class AuthenticationTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.now = localtime(None)
        cls.user = user = create_user('tester', is_superuser=True)
        cls.token = AuthToken.objects.create(user=user)

    def test_unauthenticated(self):
        request(self, '1:pool-list', status_code=401)

    def test_authenticated(self):
        request(self, '1:pool-list', headers={
            'HTTP_AUTHORIZATION': f'Bearer {self.token}',
        })

    def test_invalid_token(self):
        request(self, '1:pool-list', status_code=401, headers={
            'HTTP_AUTHORIZATION': 'Bearer not-a-uuid-id',
        })

    def test_expired_token(self):
        self.token.update(expires=self.now)

        request(self, '1:pool-list', status_code=401, headers={
            'HTTP_AUTHORIZATION': f'Bearer {self.token}',
        })
