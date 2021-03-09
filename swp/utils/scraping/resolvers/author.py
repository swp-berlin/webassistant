from playwright.async_api import ElementHandle

from .base import Resolver, create_resolver
from ..context import ScraperContext


class AuthorsResolver(Resolver):

    def __init__(self, context: ScraperContext, *args, resolver, **kwargs):
        super().__init__(context, **kwargs)
        config = {**resolver, 'key': 'authors', 'multiple': True}
        self.resolver = create_resolver(context, **config)

    async def resolve(self, node: ElementHandle, fields: dict, errors: dict):
        await self.resolver.resolve(node, fields, errors)
