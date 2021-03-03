from dataclasses import dataclass

from django.db import models
from django.utils.translation import gettext_lazy as _

from swp.models.choices import DataResolverKey, ResolverType


@dataclass
class ScraperTypeData:
    value: str
    label: str
    defaults: dict


ListWithLinkType = ScraperTypeData(
    value='list_with_link',
    label=_('List with Links'),
    defaults={
        'type': ResolverType.LIST,
        'resolvers': [
            {'type': ResolverType.URL, 'resolver': {'type': ResolverType.ATTRIBUTE, 'attribute': 'href'}},
            {
                'type': ResolverType.LINK,
                'resolvers': [
                    {'type': ResolverType.TITLE},
                    {'type': ResolverType.AUTHORS},
                    {'type': ResolverType.PUBLICATION_DATE},
                ]
            }
        ]
    }
)

ListWithLinkAndDocType = ScraperTypeData(
    value='list_with_link_and_doc',
    label=_('List with Links and Documents'),
    defaults={
        'type': ResolverType.LIST,
        'resolvers': [
            {'type': ResolverType.URL, 'resolver': {'type': ResolverType.ATTRIBUTE, 'attribute': 'href'}},
            {
                'type': ResolverType.LINK,
                'resolvers': [
                    {'type': ResolverType.TITLE},
                    {'type': ResolverType.AUTHORS},
                    {'type': ResolverType.PUBLICATION_DATE},
                    {'type':  ResolverType.DOCUMENT, 'key':  'pdf'}
                ]
            }
        ]
    }
)

ListWithDoc = ScraperTypeData(
    value='list_with_doc',
    label=_('List with Documents'),
    defaults={
        'type': ResolverType.LIST,
        'resolvers': [
            {'type': ResolverType.TITLE},
            {'type': ResolverType.AUTHORS},
            {'type': ResolverType.PUBLICATION_DATE},
            {'type':  ResolverType.DOCUMENT, 'key':  'pdf'},
        ]
    }
)

ScraperTypeChoices = [
    ListWithLinkType,
    ListWithLinkAndDocType,
    ListWithDoc,
]


class ScraperType(models.TextChoices):
    LIST_WITH_LINK = ListWithLinkType.value, ListWithLinkType.label
    LIST_WITH_LINK_AND_DOC = ListWithLinkAndDocType.value, ListWithLinkAndDocType.label
    LIST_WITH_DOC = ListWithDoc.value, ListWithDoc.label
