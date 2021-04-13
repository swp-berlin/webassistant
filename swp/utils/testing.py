from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser as User

import factory

from swp.models import Monitor, Publication, PublicationFilter, Thinktank, ThinktankFilter


def create_superuser(email: str = 'admin@localhost', **kwargs) -> User:
    return get_user_model().objects.create_superuser(email, **kwargs)


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
