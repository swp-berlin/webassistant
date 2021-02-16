from typing import Optional, Sequence, Tuple

from django.http import HttpResponse

from swp.models import Publication


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
