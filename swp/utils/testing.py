from typing import Type, Union

from django.apps import apps
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser as User

import factory
from django.core.management import call_command as django_call_command
from django.db.models import Model
from django.test import SimpleTestCase
from django.urls import reverse

from swp.models import Monitor, Publication, PublicationFilter, Thinktank, ThinktankFilter


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


class ThinktankFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'Thinktank #{n:03d}')
    description = factory.Sequence(lambda n: f'Thinktank #{n:03d} Description')
    url = factory.Sequence(lambda n: f'https://thinktank{n}/')

    class Meta:
        model = Thinktank

    @factory.post_generation
    def publications(self, create, extracted, **kwargs):
        if extracted:
            for data in extracted:
                PublicationFactory.create(thinktank=self, **data)


class PublicationFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: f'Publication #{n:03d}')
    subtitle = factory.Sequence(lambda n: f'Subtitle #{n:03d}')
    publication_date = '2020-01-01'
    url = 'https:/example.com'
    pdf_url = 'https:/example.com/download.pdf'
    pdf_pages = 42

    class Meta:
        model = Publication


class ThinktankFilterFactory(factory.django.DjangoModelFactory):
    thinktank = factory.SubFactory(ThinktankFactory)

    class Meta:
        model = ThinktankFilter

    @factory.post_generation
    def publication_filters(self, create, extracted, **kwargs):
        if extracted:
            for data in extracted:
                PublicationFilterFactory.create(thinktank_filter=self, **data)


class PublicationFilterFactory(factory.django.DjangoModelFactory):
    thinktank_filter = factory.SubFactory(ThinktankFilterFactory)

    class Meta:
        model = PublicationFilter


class MonitorFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'Monitor #{n:03d}')
    recipients = factory.List(['nobody@localhost'])

    class Meta:
        model = Monitor

    @factory.post_generation
    def thinktank_filters(self, create, extracted, **kwargs):
        if extracted:
            for data in extracted:
                ThinktankFilterFactory.create(monitor=self, **data)


def admin_url(model: Type[Model], view: str, *args, site=None, **kwargs) -> str:
    """
    Return an url to an admin view.
    """

    opts = model._meta
    site = site or admin.site
    info = site.name, opts.app_label, opts.model_name, view

    return reverse('%s:%s_%s_%s' % info, args=args, kwargs=kwargs)
