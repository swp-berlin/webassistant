from playwright.async_api import ElementHandle

from .base import Resolver
from ..context import ScraperContext


class StaticResolver(Resolver):
    def __init__(self, context: ScraperContext, *, key: str, value: str, multiple=False, **kwargs):
        super().__init__(context, **kwargs)
        self.key = key
        self.multiple = multiple
        self.value = value

    async def resolve(self, node: ElementHandle, fields: dict, errors: dict):
        if self.multiple:
            values = fields.get(self.key) or []
            fields[self.key] = [*values, self.value]
        else:
            fields[self.key] = self.value
