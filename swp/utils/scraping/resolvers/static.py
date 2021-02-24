from playwright.async_api import ElementHandle

from .base import Resolver
from ..context import ScraperContext


class StaticResolver(Resolver):
    def __init__(self, context: ScraperContext, *, key: str, value: str, **kwargs):
        super().__init__(context, **kwargs)
        self.key = key
        self.value = value

    async def resolve(self, node: ElementHandle, fields: dict, errors: dict):
        fields[self.key] = self.value
