from collections import defaultdict

from django.core.management import BaseCommand

from swp.models import Publication
from swp.utils.dateparse import parse_publication_date


class Command(BaseCommand):

    def handle(self, *args, **options):
        queryset = Publication.objects.exclude(publication_date='')
        publication_dates = queryset.values_list('publication_date', flat=True)

        parsed = 0
        failed = defaultdict(int)

        for publication_date_raw in publication_dates:
            if parse_publication_date(publication_date_raw):
                parsed += 1
            else:
                failed[publication_date_raw] += 1

        count = len(publication_dates)

        print(f'{parsed} / {count}')

        for publication_date_raw in sorted(failed):
            count = failed[publication_date_raw]

            print(f'{publication_date_raw}: {count}')
