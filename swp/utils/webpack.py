import json

from functools import lru_cache

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_mapping(path):
    """
    Returns the asset mapping on the given path.
    """

    try:
        with open(path, 'r') as fp:
            return json.load(fp)
    except FileNotFoundError:
        if settings.DEBUG:
            raise ImproperlyConfigured(f'{path} not found. Please generate assets with webpack.')

        return {}


if not settings.DEBUG:
    get_mapping = lru_cache(maxsize=None)(get_mapping)


def get_asset(name, path=None):
    """
    Returns the asset path for a given asset name.
    """

    return get_mapping(path or settings.WEBPACK_ASSETS_MAP_PATH).get(f'{name}')
