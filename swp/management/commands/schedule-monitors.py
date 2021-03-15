from django.core.management import BaseCommand

from swp.tasks.monitor import schedule_monitors


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', dest='dry_run',
                            help='Only show how many monitors would have been scheduled without sending any email')

    def handle(self, dry_run, **params):
        count = schedule_monitors(dry_run=dry_run)

        prefix = self.style.MIGRATE_HEADING('[DRY RUN] ') if dry_run else ''
        self.stdout.write(f'{prefix}Scheduling {count} monitors')
