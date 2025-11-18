from __future__ import annotations

import datetime
import os
import shutil

from contextlib import suppress
from pathlib import Path
from typing import TYPE_CHECKING, Literal, Iterator, Tuple

from django.conf import settings
from django.utils.timezone import localtime

if TYPE_CHECKING:
    from swp.models import Publication

State = Literal['todo', 'done', 'error', 'lost']
Extension = Literal['html', 'pdf', 'txt']
FileEntry = Tuple[int, Path]

DATE_FMT = '%Y-%m-%d'
SUPPORTED_EXTENSIONS = {
    '.html',
    '.pdf',
    '.txt',
}


def get_date(value: datetime.date):
    return value.strftime(DATE_FMT)


def get_filepath(directory: Path, state: State, publication: Publication, extension: Extension = 'pdf'):
    created = localtime(publication.created)
    date = get_date(created)
    timestamp = get_timestamp(created)

    return directory / state / date / f'{timestamp}-{publication.id}.{extension}'


def get_timestamp(value: datetime.datetime):
    return value.strftime('%H%M%S%f')[:-3]


def iter_files(directory: Path, state: State) -> Iterator[FileEntry]:
    directory /= state

    for date in listdir(directory):
        if is_date(date):
            for filename in listdir(directory / date):
                filepath = directory / date / filename

                if filepath.suffix in SUPPORTED_EXTENSIONS:
                    with suppress(ValueError):
                        timestamp, publication = filepath.stem.split('-')

                        yield int(publication), filepath


def listdir(directory: Path):
    try:
        filenames = os.listdir(directory)
    except FileNotFoundError:
        return []
    else:
        return sorted(filenames)


def is_date(value: str) -> bool:
    try:
        datetime.datetime.strptime(value, DATE_FMT)
    except ValueError:
        return False
    else:
        return True


def spool_file(publication: Publication, source: Path, extension: Extension, directory: Path = None) -> Path:
    return base_spool(shutil.copy, publication, source, extension, directory)


def spool_content(publication: Publication, content: str, extension: Extension, directory: Path = None) -> Path:
    return base_spool(write, publication, content, extension, directory)


def base_spool(action, publication: Publication, source, extension: Extension, directory: Path = None):
    destination = get_filepath(directory or settings.EMBEDDING_SPOOLING_DIR, 'todo', publication, extension)

    os.makedirs(destination.parent, exist_ok=True)

    return action(source, destination)


def write(content: str, destination: Path) -> Path:
    with open(destination, 'w') as fp:
        fp.write(content)

    return destination
