import os
import time

from contextlib import suppress
from pathlib import Path
from typing import Optional, Dict

from django.conf import settings
from django.core.management import BaseCommand

from swp.models import Publication
from swp.utils.spooling import State, iter_files
from swp.utils.embedding import embed
from swp.utils.timing import timed, format_duration


class Command(BaseCommand):
    directory = settings.EMBEDDING_SPOOLING_DIR
    keep_files: Dict[State, bool] = {
        'done': settings.EMBEDDING_SPOOLING_KEEP_DONE,
        'lost': settings.EMBEDDING_SPOOLING_KEEP_LOST,
        'error': settings.EMBEDDING_SPOOLING_KEEP_ERROR,
    }

    def add_arguments(self, parser):
        parser.add_argument('--directory', type=Path, default=settings.EMBEDDING_SPOOLING_DIR)
        parser.add_argument('--state', choices=['todo', *self.keep_files], default='todo')
        parser.add_argument('--page-limit', type=int, default=200)
        parser.add_argument('--force', action='store_true', default=False)
        parser.add_argument('--max-retries', type=int, default=5)

        for state, default in self.keep_files.items():
            parser.add_argument(f'--keep-{state}', action='store_true', default=default)

    def handle(self, *, state: State, force: bool, page_limit: int, max_retries: int, **options):
        self.directory = options.pop('directory', settings.EMBEDDING_SPOOLING_DIR)
        self.keep_files = {
            state: options.pop(f'keep_{state}', default)
            for state, default in self.keep_files.items()
        }

        self.stdout.write(f'Collecting files from {state}…')

        files = dict(iter_files(self.directory, state))
        count = len(files)

        if count == 0:
            return self.stdout.write('No files to process.')

        self.stdout.write(f'Processing {count} files…')

        with timed() as timer:
            self.process(files, page_limit=page_limit, force=force, max_retries=max_retries)

        duration = format_duration(timer.duration)

        self.stdout.write(f'Processed {count} files in {duration}.')

    def process(self, files: Dict[int, Path], **options):
        publications = Publication.objects.only('pdf_pages', 'embedding').in_bulk(files)

        for publication, filepath in files.items():
            self.embed(publications.get(publication), filepath, **options)

    def embed(self, publication: Optional[Publication], filepath: Path, *, page_limit=200, force=False, **options):
        filename = filepath.relative_to(self.directory)

        if publication is None:
            return self.error(filepath, 'lost', f'Publication for {filename} does not exist.')

        if page_limit and publication.pdf_pages > page_limit and not force:
            return self.error(filepath, 'error', f'{filename} exceeds page limit.')

        if publication.embedding and not force:
            return self.error(filepath, 'done', f'{filename} is already embedded.')

        self.stdout.write(f'Fetching embedding for {filename}…')

        with timed() as timer:
            success, response = self.fetch(filepath, filename, **options)

        if success:
            if response:
                publication.embedding = response
                publication.save(update_fields=['embedding'])
                self.stdout.write(f'Fetched embedding for {filename} in {timer.duration:.2f}s.')
                self.move(filepath, 'done')
            else:
                self.error(filepath, 'error', f'{filename} has no content.')

        elif success is None:
            self.stderr.write(f'Failed to fetch embedding for {filename}: {response}')

        else:
            self.stderr.write(f'Failed to fetch embedding for {filename}: [{response.status_code}] {response.text}')

            if 400 <= response.status_code < 500:
                self.move(filepath, 'error')

    def error(self, filepath: Path, state: State, msg: str):
        self.stderr.write(msg)
        self.move(filepath, state)

    def fetch(self, filepath: Path, filename: Path, *, retry=0, max_retries=5):
        success, response = embed(filepath, filename=f'{filename}')

        if success is None:
            if retry < max_retries:
                delay = 2 ** retry

                self.stderr.write(f'Fetching failed. Retrying in {delay} seconds…')
                time.sleep(delay)

                return self.fetch(filepath, filename, retry=retry + 1, max_retries=max_retries)

        return success, response

    def move(self, filepath: Path, state: State):
        parent = filepath.parent

        if self.keep_files[state]:
            directory = self.directory / state / parent.name

            os.makedirs(directory, exist_ok=True)
            filepath.replace(directory / filepath.name)
        else:
            filepath.unlink(True)

        with suppress(OSError):
            os.rmdir(parent)
