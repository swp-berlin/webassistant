from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from swp.models import Publication
from swp.utils.testing import create_user


class UserTestCase(TestCase):

    def test_can_research(self):
        content_type = ContentType.objects.get_for_model(Publication)
        perm = Permission.objects.get(codename='can_research', content_type=content_type)

        superuser = create_user('superuser', is_superuser=True)
        with_perm = create_user('with-perm')
        without_perm = create_user('without-perm')

        with_perm.user_permissions.add(perm)

        tests = [
            (superuser, True),
            (with_perm, True),
            (without_perm, False),
        ]

        for user, expected in tests:
            with self.subTest(user=user, expected=expected):
                self.assertEqual(user.can_research, expected)
