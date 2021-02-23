from enum import Enum

from .attribute import AttributeResolver
from .data import DataResolver
from .document import DocumentResolver
from .link import LinkResolver
from .list import ListResolver
from .static import StaticResolver
from .tag import TagResolver
from .author import AuthorsResolver


class ResolverType(Enum):
    List = ListResolver
    Link = LinkResolver
    Data = DataResolver
    Attribute = AttributeResolver
    Document = DocumentResolver
    Static = StaticResolver
    Tag = TagResolver
    TagData = Data
    TagAttribute = Attribute
    TagStatic = Static
    Authors = AuthorsResolver

    def create(self, context: dict, **config):
        return self.value(context, **config)
