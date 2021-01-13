from dataclasses import dataclass

from django.db import models
from django.utils.translation import gettext_lazy as _

from swp.models.choices import DataResolverKey, ResolverType


@dataclass
class ScraperTypeData:
    value: str
    label: str
    description: str
    defaults: dict


ListWithLinkType = ScraperTypeData(
    value='list_with_link',
    label=_('List with Links'),
    description=_('(paginated) Article-List with links to individual Articles which contain a single Document'),
    defaults={
        'type': ResolverType.LIST,
        'resolvers': [
            {
                'type': ResolverType.ATTRIBUTE, 'attribute': 'href', 'key': DataResolverKey.URL
            },
            {
                'type': ResolverType.LINK,
                'resolvers': [
                    {'type': ResolverType.DATA, 'key': DataResolverKey.TITLE},
                    {'type': ResolverType.DATA, 'key': DataResolverKey.AUTHOR},
                    {'type': ResolverType.DATA, 'key': DataResolverKey.PUBLICATION_DATE},
                ]
            }
        ]
    }
)

ListWithLinkAndDocType = ScraperTypeData(
    value='list_with_link_and_doc',
    label=_('List with Links and Documents'),
    description=_('(paginated) Article-List'),
    defaults={
        'type': ResolverType.LIST,
        'resolvers': [
            {
                'type': ResolverType.ATTRIBUTE, 'attribute': 'href', 'key': DataResolverKey.URL
            },
            {
                'type': ResolverType.LINK,
                'resolvers': [
                    {'type': ResolverType.DATA, 'key': DataResolverKey.TITLE},
                    {'type': ResolverType.DATA, 'key': DataResolverKey.AUTHOR},
                    {'type': ResolverType.DATA, 'key': DataResolverKey.PUBLICATION_DATE},
                    {'type':  ResolverType.DOCUMENT, 'key':  'pdf'}
                ]
            }
        ]
    }
)

ListWithDoc = ScraperTypeData(
    value='list_with_doc',
    label=_('List with Documents'),
    description=_('(paginated) Article-List'),
    defaults={
        'type': ResolverType.LIST,
        'resolvers': [
            {'type': ResolverType.DATA, 'key': DataResolverKey.TITLE},
            {'type': ResolverType.DATA, 'key': DataResolverKey.AUTHOR},
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
