from typing import Iterable, Mapping, Optional

from playwright.async_api import ElementHandle, Error as PlaywrightError

import swp.utils.scraping.resolvers.types as types

from swp.utils.scraping.context import ScraperContext
from swp.utils.scraping.exceptions import ResolverError
from swp.utils.scraping.selectors import Selector


def create_resolver(context, *, type, **config):
    return types.ResolverType[type].create(context, **config)


async def get_content(node: ElementHandle, attr: str = 'textContent'):
    _property = await node.get_property(attr)
    value = await _property.json_value()

    return value


class Resolver:

    def __init__(self, context: ScraperContext, **kwargs):
        self.context = context


class SelectorMixin:

    def __init__(self, *args, selector: Selector, multiple: bool = False, **kwargs):
        super().__init__(*args, **kwargs)
        self.selector = selector
        self.multiple = multiple

    async def get_element(self, node: ElementHandle) -> Optional[ElementHandle]:
        try:
            if self.multiple:
                elem = await node.query_selector_all(self.selector)
            else:
                elem = await node.query_selector(self.selector)

        except PlaywrightError as err:
            raise ResolverError(str(err))

        return elem


class IntermediateResolver(Resolver):

    def __init__(self, context: ScraperContext, *args, resolvers: Iterable[Mapping], **kwargs):
        super().__init__(context, **kwargs)
        self.resolvers = [create_resolver(context, **config) for config in resolvers]
