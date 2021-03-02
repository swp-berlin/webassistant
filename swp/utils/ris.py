from __future__ import annotations
from typing import Optional, Sequence, Tuple, TYPE_CHECKING

import io
from django.http import HttpResponse

if TYPE_CHECKING:
    from swp.models import Publication


RIS_MEDIA_TYPE = 'application/x-research-info-systems'


def get_ris_data(publication: Publication) -> Sequence[Tuple[str, Optional[str]]]:
    authors = publication.authors or []

    return [
        ('TY', publication.ris_type),
        ('TI', publication.title),
        ('T1', publication.subtitle),
        ('AB', publication.abstract),
        ('PY', publication.publication_date),
        ('UR', publication.url),
        ('L1', publication.pdf_url),
        ('SP', publication.pdf_pages),
        *[('AU', author) for author in authors]
    ]


def write_ris_data(response: HttpResponse, *publications):
    for publication in publications:
        for tag, value in get_ris_data(publication):
            if isinstance(value, str):
                value = value.strip()
            if value:
                response.write(f'{tag}  - {value}\n')

        response.write('ER  - \n')


def generate_ris_data(*publications) -> bytes:
    buf = io.StringIO('')
    write_ris_data(buf, *publications)

    return buf.getvalue().encode()
