import os
import shutil

from collections import defaultdict
from contextlib import suppress
from pathlib import Path

from django.conf import settings
from django.core.management import BaseCommand

from swp.utils.spooling import iter_files


class Command(BaseCommand):
    directory = settings.EMBEDDING_SPOOLING_DIR

    def add_arguments(self, parser):
        parser.add_argument('--directory', type=Path, default=settings.EMBEDDING_SPOOLING_DIR)

    def handle(self, *, directory, **options):
        dates = defaultdict(list)

        for publication, filepath in iter_files(directory, 'error'):
            dates[filepath.parent.name].append(filepath)

        count = 0

        for date, filepaths in dates.items():
            destination =  directory / 'todo' / date

            os.makedirs(destination, exist_ok=True)

            for filepath in filepaths:
                shutil.move(filepath, destination)

            with suppress(OSError):
                os.rmdir(directory / 'error' / date)

            count += len(filepaths)

        if count:
            self.stdout.write(f'Moved {count} error files back to todo.')
        else:
            self.stdout.write('No error files found.')
