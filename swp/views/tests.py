from django import test
from django.conf import settings
from django.core import mail
from django.urls import reverse
from django.utils.crypto import get_random_string

from cosmogo.utils.testing import create_user, login, request

from swp.views.auth import PasswordResetConfirmView


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

    def test_password_reset_workflow(self):
        request(self, 'password-reset:start')

        response = request(self, 'password-reset:start', expected_url='password-reset:done', email=self.user.email)
        self.assertEqual(len(mail.outbox), 1)

        uid, token = response.context.get('uid'), response.context.get('token')
        args = [uid, PasswordResetConfirmView.reset_url_token]

        url = reverse('password-reset:confirm', args=args)
        request(self, 'password-reset:confirm', args=[uid, token], expected_url=url)

        new_password = get_random_string(12)
        request(self, url, expected_url='password-reset:complete', **{
            'new_password1': new_password,
            'new_password2': new_password,
        })

        result = login(self, password=new_password)
        self.assertTrue(result)
