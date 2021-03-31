from enum import Enum

from .attribute import AttributeResolver
from .data import DataResolver
from .document import DocumentResolver
from .link import LinkResolver
from .list import ListResolver
from .static import StaticResolver
from .swp import (
    TitleResolver,
    SubtitleResolver,
    AbstractResolver,
    PublicationDateResolver,
    URLResolver,
    AuthorsResolver,
    TagsResolver,
    DOIResolver,
    ISBNResolver,
)


class ResolverType(Enum):
    List = ListResolver
    Link = LinkResolver
    Data = DataResolver
    Attribute = AttributeResolver
    Document = DocumentResolver
    Static = StaticResolver

    Title = TitleResolver
    Subtitle = SubtitleResolver
    Abstract = AbstractResolver
    Publication_Date = PublicationDateResolver
    URL = URLResolver
    Authors = AuthorsResolver
    DOI = DOIResolver
    ISBN = ISBNResolver
    Tags = TagsResolver

    def create(self, context: dict, **config):
        return self.value(context, **config)
