import json
import os

from django.conf import settings
from django.core.management import BaseCommand


class GenerateSchemeCommand(BaseCommand):
    directory = settings.BASE_DIR / 'swp' / 'assets' / 'schemes'
    filename: str

    def add_arguments(self, parser):
        parser.add_argument('--directory', dest='directory', default=self.directory)

    def handle(self, *, directory, **options):
        data = self.get_data(**options)

        os.makedirs(directory, exist_ok=True)

        with open(directory / self.filename, 'w') as fp:
            json.dump(data, fp, indent=2, sort_keys=True)

    def get_data(self, **options):
        raise NotImplementedError  # pragma: no cover
