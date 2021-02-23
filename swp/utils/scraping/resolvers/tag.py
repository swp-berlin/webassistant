from pyppeteer.element_handle import ElementHandle

from .base import Resolver, SelectorMixin, create_resolver
from ..context import ScraperContext


# FIXME
#  temporary solution that passed empty values to unused required kwargs
#  this should be better solved by splitting the selection and storage under a key into
#  dedicated resolvers that can be composed to show the intended behavior
class TagResolver(SelectorMixin, Resolver):
    def __init__(self, context: ScraperContext, *args, resolver: dict, **kwargs):
        super().__init__(context, *args, selector='', **kwargs)
        self.resolver = create_resolver(context, key='tag', **resolver)

    async def resolve(self, node: ElementHandle, fields: dict, errors: dict):
        tags = {}

        await self.resolver.resolve(node, tags, errors)

        fields.setdefault('tags', []).extend(tags.values())
