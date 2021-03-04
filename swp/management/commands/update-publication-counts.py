from sys import stdout
from django.core.management import BaseCommand
from django.db import transaction
from django.db.utils import DEFAULT_DB_ALIAS

from swp.models import Monitor


class Command(BaseCommand):
    model = Monitor

    def add_arguments(self, parser):
        parser.add_argument('--database', dest='using', default=DEFAULT_DB_ALIAS,
                            help='Alias of database to use')
        parser.add_argument('--dry-run', action='store_true', dest='dry_run',
                            help='Only show how many monitors would have been updated')

    def handle(self, using, dry_run, **options):
        verbosity = options['verbosity']
        prefix = self.style.MIGRATE_HEADING('[DRY RUN] ') if dry_run else ''
        commit = not dry_run

        with transaction.atomic(using=using):
            objects = self.get_queryset()
            count = objects.count()
            if verbosity >= 1:
                self.stdout.write(f'{prefix}Update publication counts for {count} monitors')
            if verbosity >= 2 and count:
                self.stdout.write('')
                self.stdout.write('     ID | COUNT |   NEW')
                self.stdout.write('  ----- + ----- + -----')

            for monitor in objects:
                publication_count, new_publication_count = monitor.update_publication_count(commit=commit)
                if verbosity >= 2:
                    self.stdout.write(f'  {monitor.pk: 5} | {publication_count: 5} | {new_publication_count: 5}')

    def get_queryset(self):
        return self.model.objects.select_for_update().order_by('pk')
