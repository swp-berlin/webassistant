from urllib.parse import urlparse

from django.utils.translation import gettext_lazy as _

from pyppeteer.element_handle import ElementHandle
from pyppeteer.errors import PageError

from ..browser import open_page
from ..exceptions import ResolverError
from .base import IntermediateResolver, SelectorMixin


class LinkResolver(SelectorMixin, IntermediateResolver):

    def __init__(self, *args, same_site: bool = False, **kwargs):
        super().__init__(*args, **kwargs)
        self.same_site = same_site

    async def get_href(self, node: ElementHandle) -> str:
        elem = await self.get_element(node)

        if not elem:
            raise ResolverError(_('No element matches %(selector)s') % {'selector': self.selector})

        href_property = await elem.getProperty('href')
        # noinspection PyTypeChecker
        href: str = await href_property.jsonValue()

        if not href:
            raise ResolverError(
                _('[Link Resolver] Element matching %(selector)s has no attribute href.') % {'selector': self.selector}
            )

        if self.same_site:
            url = self.context.page.url

            if urlparse(href).netloc != urlparse(url).netloc:
                raise ResolverError(_('Link %(href)s points to an external site.') % {'href': href})

        return href

    async def resolve(self, node: ElementHandle, fields: dict, errors: dict):
        href = await self.get_href(node)

        try:
            async with open_page(self.context.browser) as detail_page:
                await detail_page.goto(href)

                for resolver in self.resolvers:
                    await resolver.resolve(detail_page, fields, errors)
        except PageError as err:
            raise ResolverError(_('Failed to open %(href)s: %(error)s') % {'href': href, 'error': str(err)})
