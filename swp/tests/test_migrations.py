from django.core.management import CommandError
from django.test import TestCase

from swp.utils.testing import call_command


class MigrationTestCase(TestCase):

    def test_no_missing_or_conflicting_migrations(self):
        try:
            call_command('makemigrations', check=True, dry_run=True)
        except (CommandError, SystemExit):
            self.fail(
                'Conflicting or missing migrations. '
                'Please run makemigrations to fix the problem.'
            )
