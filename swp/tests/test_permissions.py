from django import test
from django.core.exceptions import PermissionDenied
from django.utils import timezone

from swp.models import Monitor, Scraper, ScraperType, Thinktank, User


SUPERUSER_PERMS = [
    'swp.add_user',
    'swp.change_user',
    'swp.delete_user',
    'swp.view_user',
]

MANAGER_PERMS = [
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
        cls.superuser = User.objects.get_by_natural_key('swp-superuser@localhost')
        cls.manager = User.objects.get_by_natural_key('swp-manager@localhost')
        cls.editor = User.objects.get_by_natural_key('swp-editor@localhost')

        cls.thinktank = Thinktank.objects.create(
            name='PIIE',
            url='https://www.piie.com/',
            unique_field='T1-AB',
            created=now,
        )

        cls.scraper_type = ScraperType.objects.create(name='Test Type', config={'how-to': 'scrape'})
        cls.scraper = Scraper.objects.create(
            type=cls.scraper_type,
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

    def test_superuser_permissions(self):
        self.assertTrue(self.superuser.has_perms(SUPERUSER_PERMS))

    def test_manager_permissions(self):
        self.assertTrue(self.manager.has_perms(MANAGER_PERMS))

        self.assertTrue(self.thinktank.can_activate(user=self.manager))
        self.assertTrue(self.thinktank.can_deactivate(user=self.manager))

    def test_editor_permissions(self):
        self.assertTrue(self.editor.has_perms(EDITOR_PERMS))

        self.assertTrue(self.monitor.can_activate(user=self.editor))
        self.assertTrue(self.monitor.can_deactivate(user=self.editor))

    ##############
    # ACTIVATION #
    ##############

    def test_monitor_activation(self):
        self.assertTrue(self.monitor.is_active)

        self.monitor.deactivate(user=self.editor)
        self.assertFalse(self.monitor.is_active)
        self.monitor.activate(user=self.editor)
        self.assertTrue(self.monitor.is_active)

        with self.assertRaises(PermissionDenied):
            self.monitor.deactivate(user=self.manager)
        with self.assertRaises(PermissionDenied):
            self.monitor.deactivate(user=self.superuser)

    def test_thinktank_activation(self):
        self.assertTrue(self.thinktank.is_active)

        self.thinktank.deactivate(user=self.manager)
        self.assertFalse(self.thinktank.is_active)
        self.thinktank.activate(user=self.manager)
        self.assertTrue(self.thinktank.is_active)

        with self.assertRaises(PermissionDenied):
            self.thinktank.deactivate(user=self.editor)
        with self.assertRaises(PermissionDenied):
            self.thinktank.deactivate(user=self.superuser)

