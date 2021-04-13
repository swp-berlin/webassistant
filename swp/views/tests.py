from django import test
from django.conf import settings
from django.core import mail
from django.urls import reverse
from django.utils.crypto import get_random_string

from cosmogo.utils.testing import create_user, login, request

from swp.api.serializers import UserSerializer
from swp.models import User
from swp.views.auth import PasswordResetConfirmView
from swp.tests.test_permissions import EDITOR_PERMS, MANAGER_PERMS


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


class UserDataTestCase(test.TestCase):
    fixtures = ['groups', 'test-users']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get_by_natural_key('admin@localhost')
        cls.user_data = UserSerializer(cls.user).data

        cls.manager = User.objects.get_by_natural_key('swp-manager@localhost')
        cls.editor = User.objects.get_by_natural_key('swp-editor@localhost')

    def fetch_user_data(self, user: User = None) -> dict:
        login(self, user)
        response = request(self, 'index')

        # TODO Parse #user-data from returned HTML ..
        return response.context['user_data']

    def test_user_data(self):
        user_data = self.fetch_user_data()

        self.assertEqual(user_data, self.user_data)
        self.assertEqual(user_data['email'], self.user.email)
        self.assertIn('permissions', user_data)

    def check_user_perms(self, user, perm_list):
        user_data = self.fetch_user_data(user)
        for perm in perm_list:
            self.assertIn(perm, user_data['permissions'], f'Permission {perm} missing for {user}')

    def test_manager_permissions(self):
        self.check_user_perms(self.manager, MANAGER_PERMS)

    def test_editor_permissions(self):
        self.check_user_perms(self.editor, EDITOR_PERMS)
