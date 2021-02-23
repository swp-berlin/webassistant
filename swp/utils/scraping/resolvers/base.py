from typing import Iterable, Mapping, Optional

from pyppeteer.element_handle import ElementHandle
from pyppeteer.errors import ElementHandleError

import swp.utils.scraping.resolvers.types as types

from swp.utils.scraping.context import ScraperContext
from swp.utils.scraping.exceptions import ResolverError
from swp.utils.scraping.selectors import Selector


def create_resolver(context, *, type, **config):
    return types.ResolverType[type].create(context, **config)


async def get_content(node, attr: str = 'textContent'):
    text_content_property = await node.getProperty(attr)
    text = await text_content_property.jsonValue()

    return text


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
                elem = await node.querySelectorAll(self.selector)
            else:
                elem = await node.querySelector(self.selector)

        except ElementHandleError as err:
            raise ResolverError(str(err))

        return elem


class IntermediateResolver(Resolver):

    def __init__(self, context: ScraperContext, *args, resolvers: Iterable[Mapping], **kwargs):
        super().__init__(context, **kwargs)
        self.resolvers = [create_resolver(context, **config) for config in resolvers]
