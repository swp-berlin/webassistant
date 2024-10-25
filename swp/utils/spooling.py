from __future__ import annotations

import datetime
import os

from contextlib import suppress
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from django.utils.timezone import localtime

if TYPE_CHECKING:
    from swp.models import Publication


DATE_FMT = '%Y-%m-%d'
EXTENSION = Literal['html', 'pdf', 'txt']
SUPPORTED_EXTENSIONS = {
    '.html',
    '.pdf',
    '.txt',
}


def get_filepath(directory: Path, publication: Publication, extension: EXTENSION = 'pdf'):
    created = localtime(publication.created)
    date = created.strftime(DATE_FMT)
    timestamp = get_timestamp(created)

    return directory / date / f'{timestamp}-{publication.id}.{extension}'


def get_timestamp(value: datetime.datetime):
    return value.strftime('%H%M%S%f')[:-3]


def iter_files(directory: Path):
    for date in sorted(os.listdir(directory)):
        if is_date(date):
            for filename in sorted(os.listdir(directory / date)):
                filepath = directory / date / filename

                if filepath.suffix in SUPPORTED_EXTENSIONS:
                    with suppress(ValueError):
                        timestamp, publication = filepath.stem.split('-')

                        yield int(publication), filepath


def is_date(value: str) -> bool:
    try:
        datetime.datetime.strptime(value, DATE_FMT)
    except ValueError:
        return False
    else:
        return True
