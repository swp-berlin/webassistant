from pathlib import Path

import pikepdf

from django.conf import settings
from django.core.management import BaseCommand

from swp.models import Publication
from swp.utils import spooling
from swp.utils.html import is_html


def iter_files(directory: Path):
    for publication, filepath in spooling.iter_files(directory):
        if filepath.suffix == '.pdf':
            yield publication, filepath


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--directory', type=Path, default=settings.EMBEDDING_SPOOLING_DIR)

    def handle(self, *, directory: Path, **options):
        files = dict(iter_files(directory))
        queryset = Publication.objects.filter(id__in=files, embedding=None)

        for publication, url in queryset.values_list('id', 'pdf_url'):
            filepath = files[publication]

            try:
                with pikepdf.open(filepath) as pdf:
                    pages = len(pdf.pages)
            except pikepdf.PdfError as error:
                pages, filename = 0, f'{filepath.parent.name}/{filepath.name}'

                if is_html(filepath):
                    self.stderr.write(f'File {filename} is HTML.')
                    target = filepath.with_suffix('.html')
                else:
                    self.stderr.write(f'Invalid PDF ({filename}): {error}')
                    target = filepath.with_suffix('.pdf.inv')

                filepath.rename(target)

            count = Publication.objects.filter(pdf_url=url).update(embedding=[pages])

            self.stdout.write(f'Updated {count} publications with PDF {url} to an embedding of {pages} pages.')
