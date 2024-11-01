import random
import string

from contextlib import contextmanager
from typing import Union, Protocol

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser as User
from django.contrib.auth.models import Group

from django.core.management import call_command as django_call_command
from django.test import SimpleTestCase
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.text import slugify

from swp.models import Monitor, Pool, Thinktank, Scraper, ScraperError
from swp.utils.domain import get_canonical_domain

Args = Union[tuple, list]


def call_command(*args, **kwargs):
    """
    Silence all output of commands.
    """

    with open('/dev/null', 'w') as devnull:
        defaults = dict(stdout=devnull, stderr=devnull)
        defaults.update(kwargs)

        return django_call_command(*args, **defaults)


def create_user(username: str, **kwargs):
    model = apps.get_model(settings.AUTH_USER_MODEL)
    password = kwargs.setdefault('password', 'P4sSW0rD')

    kwargs.setdefault('email', f'{username}@test.case')
    kwargs.setdefault(model.USERNAME_FIELD, username)

    user = model.objects.create_user(**kwargs)

    user.raw_password = password

    return user


def create_superuser(email: str = 'admin@localhost', **kwargs) -> User:
    return get_user_model().objects.create_superuser(email, **kwargs)


def add_to_group(user, name: str):
    group = Group.objects.get(name=name)

    return user.groups.add(group)


def get_url(url: str, args: Args = None, kwargs: dict = None) -> str:
    """
    Helper to reverse the given url name.
    """

    return url if url.startswith('/') else reverse(url, args=args, kwargs=kwargs)


def get_handler(test_case: SimpleTestCase, method: str = None, **data):
    if data:
        method = str.lower(method or 'POST')
    else:
        method = str.lower(method or 'GET')

    return getattr(test_case.client, method)


def login(test_case: SimpleTestCase, user=None, password: str = None) -> bool:
    """
    Logs in the user trying to use the raw password or the given password.
    Force logs in the user when no password is found.
    """

    user = user or getattr(test_case, 'user')
    password = password or getattr(user, 'raw_password', password)

    if password is None:
        return test_case.client.force_login(user=user) or True

    return test_case.client.login(username=user.username, password=password)


def request(test_case: SimpleTestCase, url: str, status_code: int = None, expected_url: str = None,
            args: Args = None, kwargs: dict = None, headers: dict = None, msg: str = None, **data):
    """
    A helper to make a request with the test case's http client.

    The given args and kwargs are used to reverse the url
    but not the expected url. When expected url needs
    args/kwargs pass an absolute url instead.

    All additional kwargs are passed as post parameters.
    When posting without parameters just pass post=True.
    """

    handler = get_handler(test_case, **data)
    url = get_url(url, args, kwargs)
    headers = headers or {}

    response = handler(url, data=data or None, **headers)

    status_code = status_code or 200
    msg = msg or getattr(response, 'content', None)

    if expected_url:
        test_case.assertRedirects(
            response=response,
            expected_url=get_url(expected_url),
            target_status_code=status_code,
        )
    else:
        test_case.assertEqual(response.status_code, status_code, msg=msg)

    return response


@contextmanager
def override_dns_name(new_dns_name: str, *, attr='_fqdn'):
    """
    This context manager can be used to prefill the DNS name cache to avoid long timeouts on local machines.
    """

    from django.core.mail import DNS_NAME

    old_dns_name = getattr(DNS_NAME, attr, None)

    setattr(DNS_NAME, attr, new_dns_name)

    try:
        yield old_dns_name
    finally:
        if old_dns_name:
            setattr(DNS_NAME, attr, old_dns_name)
        else:
            delattr(DNS_NAME, attr)


def create_monitor(**kwargs) -> Monitor:
    defaults = {
        'pool': Pool(id=0),
        'name': 'Test-Monitor',
        'query': 'test',
        'is_active': True,
        'recipients': [],
    }

    defaults.update(kwargs)

    return Monitor.objects.create(**defaults)


def create_thinktank(name=None, domain=None, url=None, **kwargs) -> Thinktank:
    if name is None:
        name = 'Thinktank %s' % get_random_string(6, string.ascii_letters)

    if domain is None:
        domain = get_canonical_domain(url) if url else '%s.com' % slugify(name)

    if url is None:
        url = domain and f'https://www.{domain}'

    defaults = {
        'name': name,
        'pool': Pool(id=0),
        'domain': domain,
        'url': url,
        'is_active': True,
    }

    defaults.update(kwargs)

    return Thinktank.objects.create(**defaults)


def create_scraper(thinktank: Thinktank, **kwargs) -> Scraper:
    defaults = {
        'thinktank': thinktank,
        'start_url': thinktank.url,
        'data': {},
    }

    defaults.update(kwargs)

    return Scraper.objects.create(**defaults)


SCRAPER_ERROR_FIELDS = [
    '',
    'url',
    'title',
    'subtitle',
    'abstract',
]

SCRAPER_ERROR_CODES = [
    '',
    'missing',
    'invalid',
]


def create_scraper_error(scraper, *, code: str = None, field: str = None, **kwargs) -> ScraperError:
    code = code or random.choice(SCRAPER_ERROR_CODES)
    field = field or random.choice(SCRAPER_ERROR_FIELDS)

    defaults = {
        'scraper': scraper,
        'code': code,
        'field': field,
        'message': f'{code} {field}',
    }

    defaults.update(kwargs)

    return ScraperError.objects.create(**defaults)


def get_random_embedding_vector(dims: int, *, signs=(+1, -1)):
    return [random.random() * random.choice(signs) for _ in range(dims)]


class Cache(Protocol):

    def cache_clear(self): ...


@contextmanager
def clear_cache(cache: Cache):
    try:
        yield cache
    finally:
        cache.cache_clear()
