from django import test
from django.conf import settings
from django.urls import reverse

from cosmogo.utils.testing import create_user, login, request


class AuthViewTestCase(test.TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = create_user('user')
        cls.index_url = reverse('index')

    def test_redirect_to_login(self):
        expected_url = f'{settings.LOGIN_URL}?next={self.index_url}'

        request(self, self.index_url, expected_url=expected_url)

    def test_logged_in(self):
        login(self)

        request(self, self.index_url)
