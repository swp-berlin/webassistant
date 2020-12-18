from typing import Iterable

from django import test
from django.core.exceptions import PermissionDenied
from django.utils import timezone

from swp.models import (
    ActivatableModel,
    Monitor,
    Scraper,
    Thinktank,
    User,
)
from swp.models.choices import ScraperType


USERADMIN_PERMS = [
    'swp.add_user',
    'swp.change_user',
    'swp.delete_user',
    'swp.view_user',
]

MANAGER_PERMS = [
    'swp.activate_scraper',
    'swp.add_scraper',
    'swp.change_scraper',
    'swp.deactivate_scraper',
    'swp.delete_scraper',
    'swp.view_scraper',
    'swp.view_scrapererror',

    'swp.activate_thinktank',
    'swp.add_thinktank',
    'swp.change_thinktank',
    'swp.deactivate_thinktank',
    'swp.delete_thinktank',
    'swp.view_thinktank',
]

EDITOR_PERMS = [
    'swp.activate_monitor',
    'swp.add_monitor',
    'swp.change_monitor',
    'swp.deactivate_monitor',
    'swp.delete_monitor',
    'swp.view_monitor',
]


class PermissionTestCase(test.TestCase):
    fixtures = ['groups', 'test-users']

    @classmethod
    def setUpTestData(cls):
        cls.now = now = timezone.localtime()
        cls.user = User.objects.get_by_natural_key('admin@localhost')
        cls.useradmin = User.objects.get_by_natural_key('swp-useradmin@localhost')
        cls.manager = User.objects.get_by_natural_key('swp-manager@localhost')
        cls.editor = User.objects.get_by_natural_key('swp-editor@localhost')

        cls.thinktank = Thinktank.objects.create(
            name='PIIE',
            url='https://www.piie.com/',
            unique_field='T1-AB',
            created=now,
        )

        cls.scraper = Scraper.objects.create(
            type=ScraperType.LIST_WITH_DOCS.value,
            thinktank=cls.thinktank,
            data={'scraped': True},
            start_url='https://www.piie.com/research/publications/policy-briefs',
            checksum='de9474fa85634623fd9ae9838f949a02c9365ede3499a26c9be52363a8b7f214',
            created=now,
        )

        cls.monitor = Monitor.objects.create(
            name='Monitor Sergejewitsch Gorbatschow',
            recipients=['the-party@localhost'],
            created=now,
        )

    def test_useradmin_permissions(self):
        self.assertTrue(self.useradmin.has_perms(USERADMIN_PERMS))

    def test_manager_permissions(self):
        self.assertTrue(self.manager.has_perms(MANAGER_PERMS))

        self.assertTrue(self.scraper.can_activate(user=self.manager))
        self.assertTrue(self.scraper.can_deactivate(user=self.manager))

        self.assertTrue(self.thinktank.can_activate(user=self.manager))
        self.assertTrue(self.thinktank.can_deactivate(user=self.manager))

    def test_editor_permissions(self):
        self.assertTrue(self.editor.has_perms(EDITOR_PERMS))

        self.assertTrue(self.monitor.can_activate(user=self.editor))
        self.assertTrue(self.monitor.can_deactivate(user=self.editor))

    ##############
    # ACTIVATION #
    ##############

    def assert_activation(self, obj: ActivatableModel, user: User, deny: Iterable[User] = ()):
        """ Assert activation and deactivation operations behave according to spec. """
        self.assertTrue(obj.is_active)

        obj.deactivate(user=user)
        self.assertFalse(obj.is_active)

        obj.activate(user=user)
        self.assertTrue(obj.is_active)

        for deny_user in deny:
            with self.assertRaises(PermissionDenied):
                obj.deactivate(user=deny_user)
            with self.assertRaises(PermissionDenied):
                obj.activate(user=deny_user)

        # Denied operations should not alter model state
        self.assertTrue(obj.is_active)

    def test_monitor_activation(self):
        self.assert_activation(self.monitor, self.editor, [self.manager, self.useradmin])

    def test_scraper_activation(self):
        self.assert_activation(self.scraper, self.manager, [self.editor, self.useradmin])

    def test_thinktank_activation(self):
        self.assert_activation(self.thinktank, self.manager, [self.editor, self.useradmin])

