from typing import Type, cast

from django.db.models import Model
from django.utils import translation

from drf_spectacular.plumbing import get_doc
from drf_spectacular.utils import extend_schema
from drf_spectacular.views import SpectacularAPIView as BaseSpectacularAPIView, SCHEMA_KWARGS

from swp.api.v1 import default_router
from swp.models import Category, Monitor, Pool, Publication, PublicationList, Scraper, Thinktank

__all__ = [
    'SWPSpectacularAPIView',
]


@default_router.register('schema')
class SWPSpectacularAPIView(BaseSpectacularAPIView):

    @extend_schema(**{**SCHEMA_KWARGS, 'parameters': None})
    @translation.override('en')
    def get(self, request, *args, **kwargs):
        return BaseSpectacularAPIView.get(self, request, *args, **kwargs)


def get_tag(model):
    if isinstance(model, tuple):
        model, name = model
    else:
        name = cast(Type[Model], model)._meta.model_name

    return {
        'name': name,
        'description': get_doc(model),
    }


MODELS = [
    Category,
    Monitor,
    Pool,
    Publication,
    (PublicationList, 'publication-list'),
    Scraper,
    Thinktank,
]


TAGS = [get_tag(model) for model in MODELS]


def add_root_tags(result, **kwargs):
    result['tags'] = TAGS

    return result
