from typing import List, Type, cast

from django.db import models
from django.utils.text import get_text_list

from drf_spectacular.authentication import SessionScheme, TokenScheme
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.plumbing import get_doc

from swp.models import *
from swp.utils.text import paragraph

from .viewsets import SWPViewSet

SessionScheme.match_subclasses = TokenScheme.match_subclasses = True

ModelType = Type[models.Model]

ACTION_DESCRIPTIONS = {
    'list': 'retrieve a list of',
    'partial_update': 'partially update',
    'destroy': 'delete',
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


def get_tag(model):
    if isinstance(model, tuple):
        model, name = model
    else:
        name = cast(ModelType, model)._meta.model_name

    return {
        'name': name,
        'description': get_doc(model),
    }


TAGS = [get_tag(model) for model in MODELS]


def add_root_tags(result, **kwargs):
    result['tags'] = TAGS

    return result


class SWPSchema(AutoSchema):

    def is_excluded(self) -> bool:
        return 'v1' not in self.path

    def _tokenize_path(self) -> List[str]:
        """
        Remove the v1 prefix from tokenized path.
        """

        prefix, *tokenized_path = AutoSchema._tokenize_path(self)

        return tokenized_path

    def get_operation_id(self) -> str:
        operation_id = AutoSchema.get_operation_id(self)

        if isinstance(self.view, SWPViewSet):
            if self.view.action not in self.method_mapping.values():
                action = self.method_mapping[self.method.lower()]

                return operation_id.removesuffix(f'_{action}')

        return operation_id

    def get_summary(self) -> str:
        return self.path

    def get_description(self) -> str:
        if description := AutoSchema.get_description(self):
            return description

        action: str = self.view.action
        description = ACTION_DESCRIPTIONS.get(action, action)
        model: ModelType = self.view.queryset.model
        opts = model._meta

        if self._is_list_view(None):
            description = f'Endpoint to {description} {opts.verbose_name_plural}.'
        else:
            description = f'Endpoint to {description} a {opts.verbose_name}.'

        def add(*sentences):
            return paragraph(description, *sentences)

        if action == 'create':
            if issubclass(model, ActivatableModel):
                description = add(
                    f'Newly created {opts.verbose_name_plural} are inactive by default.',
                    f'Refer to `/api/v1/{opts.model_name}/{{id}}/activate/` to activate a {opts.verbose_name}.',
                )

        elif action == 'destroy':
            if relations := self.get_protected_relations(model):
                verbose_name_plural = str.capitalize(f'{opts.verbose_name_plural}')
                description = add(f'{verbose_name_plural} that are still referenced by {relations} cannot be deleted.')

        elif action.endswith('update'):
            if model is Scraper:
                description = add(
                    f'Only deactivated {opts.verbose_name_plural} may be updated, an error will be thrown otherwise.',
                    f'Refer to `/api/v1/{opts.model_name}/{{id}}/deactivate/` to deactivate a {opts.verbose_name} before updating.',
                )

        return description

    @staticmethod
    def get_protected_relations(model: ModelType):
        return get_text_list([
            cast(ModelType, related_object.related_model)._meta.verbose_name_plural
            for related_object in model._meta.related_objects
            if related_object.on_delete is models.PROTECT
        ])
