import mimetypes
import posixpath

from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from django.conf import settings

from swp.utils.requests import TimeOutSession

TIMEOUT = 3.05, None


def get_url(endpoint: str, filename: str = None, *, version: int = 1):
    scheme, netloc, path, query, fragment = urlsplit(settings.EMBEDDING_API_HOST)
    path = posixpath.join('api', f'v{version}', endpoint, filename or '')
    components = scheme, netloc, path, query, fragment

    return urlunsplit(components)


def request(method, url, **kwargs):
    with TimeOutSession(TIMEOUT) as session:
        return session.json(method, url, **kwargs)


def embed(filepath: Path, *, filename: str = None, content_type: str = None, **headers):
    url = get_url('embedding', filename or filepath.name)

    if content_type is None:
        content_type, encoding = mimetypes.guess_type(filepath)

    if content_type:
        headers.setdefault('Content-Type', content_type)

    with open(filepath, 'rb') as fp:
        return request('PUT', url, data=fp, headers=headers)


def embed_query(query: str):
    return request('GET', get_url('query-embed'), params={'query': query})
