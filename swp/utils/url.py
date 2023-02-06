import posixpath

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import resolve_url


def get_secure(secure=None):
    if secure is None:
        return not settings.DEBUG

    return secure


def get_absolute_url(request, view_name, *args, secure=None, **kwargs):
    location = resolve_url(view_name, *args, **kwargs)

    if request is None:
        site = get_current_site(request=None)
        domain = site.domain.rstrip(posixpath.sep)
        scheme = 'https' if get_secure(secure) else 'http'

        return f'{scheme}://{domain}{location}'

    return request.build_absolute_uri(location)
