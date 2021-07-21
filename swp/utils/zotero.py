import datetime
from typing import Any, Iterable, List, Mapping, Optional
from django.conf import settings

from swp.models import Publication


def get_zotero_author_data(author):
    return {
        'creatorType': 'author',
        'firstName': '',
        'lastName': author,
    }


OBJECT_KEY_ALPHABET = 'ABCDEFGHIJKLMNPQRSTUVWXYZ23456789'


def encode_object_key(value: int, *, initial: str = '') -> str:
    assert isinstance(value, int), 'Value must be an integer'
    assert value >= 0, 'Value must be greater zero'
    assert not initial or len(initial) >= 8, 'Initial block must be 8 characters long'

    encoded = initial or 'SWPZTAPI'

    while value:
        value, index = divmod(value, 33)
        encoded = OBJECT_KEY_ALPHABET[index] + encoded

    return encoded[:8]


def get_zotero_object_key(publication) -> str:
    """ Get fixed width alpha-numeric local identifier. """
    return encode_object_key(publication.pk)


def format_datetime(dt: Optional[datetime.datetime]) -> Optional[str]:
    return dt.isoformat(timespec='seconds') if dt else None


def get_zotero_attachment_data(publication: Publication) -> Mapping[str, Any]:
    object_key = get_zotero_object_key(publication)

    return {
        'parentItem': object_key,
        'itemType': 'attachment',
        'linkMode': 'linked_url',
        'url': publication.pdf_url,
    }


def get_zotero_publication_data(publication: Publication) -> Mapping[str, Any]:
    authors = publication.authors or []
    creators = [get_zotero_author_data(author) for author in authors]
    title = f'{publication.title}: {publication.subtitle}' if publication.subtitle else publication.title
    object_key = get_zotero_object_key(publication)

    return {
        'key': object_key,  # Local key required for attachments
        'version': 0,  # Must be set when using `key`
        'itemType': 'book',
        'title': title,
        'creators': creators,
        'abstractNote': publication.abstract,
        'series': '',
        'seriesNumber': '',
        'volume': '',
        'numberOfVolumes': '',
        'edition': '',
        'place': '',
        'publisher': '',
        'date': format_datetime(publication.publication_date),
        'numPages': publication.pdf_pages,
        'language': '',
        'ISBN': publication.isbn,
        'shortTitle': publication.title if publication.subtitle else '',
        'url': publication.url,
        'accessDate': format_datetime(publication.last_access),
        'archive': '',
        'archiveLocation': '',
        'libraryCatalog': '',
        'callNumber': '',
        'rights': ', '.join(publication.tags),  # [SWP-167] TODO Excel says to store under "rights" -- but why?
        'extra': f'DOI: {publication.doi}' if publication.doi else '',
        'tags': [
            {'tag': tag} for tag in publication.tags
        ],
        'collections': [],
        'relations': {}
    }


def get_zotero_data(publications: Iterable[Publication]) -> List[Mapping[str, Any]]:
    data = []
    for publication in publications:
        data.append(get_zotero_publication_data(publication))
        if publication.pdf_url:
            data.append(get_zotero_attachment_data(publication))

    return data


def get_zotero_api_headers(api_key: str, *, version: int = None) -> Mapping[str, Any]:
    if version is None:
        version = settings.ZOTERO_API_VERSION

    return {
        'Authorization': f'Bearer {api_key}',
        'Zotero-API-Version': f'{version}',
    }


def build_zotero_api_url(path: str) -> str:
    base_url = settings.ZOTERO_API_BASE_URL
    path = path.lstrip('/')

    return f'{base_url}/{path}'
