from dataclasses import dataclass

from django.utils.translation import gettext_lazy as _


@dataclass
class ScraperType:
    name: str
    description: str
    resolver: [dict]


ListType = ScraperType(
    name=_('List with Documents'),
    description=_('(paginated) Article-List with links to individual Articles which contain a single Document'),
    resolver={
        'type': 'list',
        'resolvers': [
            {
                'type': 'Attribute', 'attribute': 'href', 'key': 'url'
            },
            {
                'type': 'link',
                'config': {
                    'resolvers': [
                        {'type': 'Data', 'key': 'title'},
                        {'type': 'data', 'key': 'abstract'},
                        {'type': 'data', 'key': 'author'},
                        {'type': 'data', 'key': 'publication_date'},
                        {'type':  'document', 'key':  'pdf'}
                    ]
                }
            }
        ]
    }

)
