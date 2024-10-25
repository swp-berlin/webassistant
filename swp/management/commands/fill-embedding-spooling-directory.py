import os
import random
import shutil
import subprocess
import sys

from contextlib import contextmanager, suppress
from pathlib import Path
from typing import List
from urllib.parse import urlsplit

from django.conf import settings
from django.core.management import BaseCommand, CommandError

from swp.models import Publication
from swp.utils import spooling

EXCLUDED = [
    'd2071andvip0wj.cloudfront.net',
    'doc-research.org',
    'media.africaportal.org',
    'www.easo.europa.eu',
    'www.foi.se',
    'www.imisem.info',
    'www.knomad.org',
]


@contextmanager
def cleanup(filepath: Path):
    try:
        yield filepath
    finally:
        with suppress(FileNotFoundError):
            os.unlink(filepath)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--directory', type=Path, default=settings.EMBEDDING_SPOOLING_DIR)
        parser.add_argument('--limit', type=int, default=0,
                            help='Number of URLs to download.')
        parser.add_argument('--retry', type=int, default=2,
                            help='Number of retries for each URL.')
        parser.add_argument('--parallel-max', dest='parallel', type=int, default=8,
                            help='Number of parallel downloads.')
        parser.add_argument('--force', action='store_true', default=False,
                            help='Include publications already having an embedding.')
        parser.add_argument('-e', '--exclude', action='extend', nargs='*', default=[],
                            help='Exclude URLs with the given hostname(s).')
        parser.add_argument('--no-default-exclude', action='store_true', default=False,
                            help='Do not use default exclude list.')

    def handle(self, *, directory: Path, limit: int, retry: int, parallel: int, exclude: List[str], **options):
        if not shutil.which('curl'):
            raise CommandError('You need curl in order to use this command.')

        urls = {}

        if options.get('no_default_exclude'):
            exclude = set(exclude)
        else:
            exclude = set(exclude + EXCLUDED)

        queryset = Publication.objects.filter(pdf_pages__gt=0).order_by('created', 'id')

        if not options.get('force'):
            queryset = queryset.filter(embedding=None)

        for publication, url, created in queryset.values_list('id', 'pdf_url', 'created'):
            result = urlsplit(url)

            if result.hostname in exclude:
                continue

            publication = Publication(id=publication, pdf_url=url, created=created)
            urls[url] = spooling.get_filepath(directory, publication, 'pdf')

        if not urls:
            return self.stdout.write('No PDF files to download…')

        tasks = [*urls]
        count = len(tasks)

        if limit and limit < count:
            count, tasks = limit, random.sample(tasks, k=limit)
        else:
            random.shuffle(tasks)

        os.makedirs(directory, exist_ok=True)

        with cleanup(directory / f'curl.tasks') as filepath:
            with open(filepath, 'w') as fp:
                for url in tasks:
                    filepath = urls[url]

                    fp.write(f'url = {url}{os.linesep}')
                    fp.write(f'output = {filepath}{os.linesep}')

            cmd = [
                'curl',
                '--retry', f'{retry}',
                '--retry-connrefused',
                '--parallel',
                '--parallel-max', f'{parallel}',
                '--create-dirs',
                '--location',  # follow redirects
                '--fail',  # do not write files on 4XX and 5XX
                '--config', f'{fp.name}',
            ]

            self.stdout.write(f'Starting to curl {count} PDFs…')

            status = subprocess.call(cmd)

            sys.exit(status)
