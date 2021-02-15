import asyncio
import os
import pathlib
from enum import Enum
from typing import Mapping, Iterable, Optional
from urllib.parse import urlparse

import pikepdf
from pyppeteer.element_handle import ElementHandle
from pyppeteer.errors import ElementHandleError, PageError

from django.utils.translation import gettext_lazy as _

from .browser import open_page
from .context import ScraperContext
from .exceptions import ErrorLevel, ResolverError
from .paginators import PaginatorType
from .selectors import Selector
from .utils import get_error


class Resolver:

    def __init__(self, context: ScraperContext, **kwargs):
        self.context = context


class SelectorMixin:

    def __init__(self, *args, selector: Selector, **kwargs):
        super().__init__(*args, **kwargs)
        self.selector = selector

    async def get_element(self, node: ElementHandle) -> Optional[ElementHandle]:
        try:
            elem = await node.querySelector(self.selector)
        except ElementHandleError as err:
            raise ResolverError(str(err))

        return elem


class IntermediateResolver(Resolver):

    def __init__(self, context: ScraperContext, *args, resolvers: Iterable[Mapping], **kwargs):
        super().__init__(context, **kwargs)
        self.resolvers = [self.create_resolver(context, **config) for config in resolvers]

    @staticmethod
    def create_resolver(context, *, type, **config):
        return ResolverType[type].create(context, **config)


class ListResolver(IntermediateResolver):
    """
    Resolves every node selected by the given :selector by calling every resolver in the :resolvers list
    """

    def __init__(self, context, *args, selector: str, paginator: dict = None,
                 **kwargs):
        super().__init__(context, *args, **kwargs)

        if paginator:
            self.paginator = self.create_paginator(context, item_selector=selector, **paginator)
            self.selector = f'{paginator["list_selector"]} {selector}'
        else:
            self.selector = selector

    @staticmethod
    def create_paginator(context, *, type, **paginator):
        return PaginatorType[type].create(context, **paginator)

    async def resolve(self) -> [dict]:
        async for node in self.resolve_nodes():
            detail_context = await self.resolve_node(node)

            yield detail_context

    async def resolve_nodes(self):
        if self.paginator:
            async for node in self.paginator.get_nodes():
                yield node
        else:
            nodes = await self.context.page.querySelectorAll(self.selector)

            if not nodes:
                raise ResolverError(
                    _('No elements matching %(selector)s found') % {'selector': self.selector}
                )

            for node in nodes:
                yield node

    async def resolve_node(self, node: ElementHandle):
        fields = {}
        errors = {}

        for resolver in self.resolvers:
            await resolver.resolve(node, fields, errors)

        return {'fields': fields, 'errors': errors}


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


class DataResolver(SelectorMixin, Resolver):

    def __init__(self, *args, key: str, required: bool = False, **kwargs):
        super().__init__(*args, **kwargs)
        self.required = required
        self.key = key

    async def resolve(self, node: ElementHandle, fields: dict, errors: dict):
        try:
            await self._resolve(node, fields, errors)
        except ResolverError as err:
            errors[self.key] = get_error(err)

    async def _resolve(self, node: ElementHandle, fields: dict, errors: dict):
        elem = await self.get_element(node)

        if not elem:
            raise ResolverError(
                _('No element matches %(selector)s') % {'selector': self.selector},
                level=ErrorLevel.ERROR if self.required else ErrorLevel.WARNING
            )

        await self.handle_element(elem, fields)

    async def handle_element(self, elem: ElementHandle, fields: dict):
        text = await self.get_content(elem)

        fields[self.key] = text

    async def get_content(self, elem):
        text_content_property = await elem.getProperty('textContent')
        text = await text_content_property.jsonValue()

        return text


class AttributeResolver(DataResolver):

    def __init__(self, *args, attribute, **kwargs):
        super().__init__(*args, **kwargs)
        self.attribute = attribute

    async def get_content(self, elem):
        attribute = await elem.getProperty(self.attribute)
        content = await attribute.jsonValue()

        if not content:
            raise ResolverError(
                _('[Attribute Resolver] Element matching %(selector)s has no attribute %(attribute)s') % {
                    'selector': self.selector,
                    'attribute': self.attribute
                }
            )

        return content


DOWNLOAD_TEMPLATE = """
    () => {
        const dl_link = document.createElement("a");
        dl_link.href = '%s';
        dl_link.download = '%s';
        dl_link.click();
    }
"""


class DocumentResolver(DataResolver):

    async def get_element(self, node: ElementHandle) -> Optional[ElementHandle]:
        try:
            [elem, *other] = await node.querySelectorAll(self.selector)
        except ElementHandleError as err:
            raise ResolverError(str(err))

        if other:
            raise ResolverError(_('%(selector)s matches more than one document.') % {'selector': self.selector})

        return elem

    async def handle_element(self, elem: ElementHandle, fields: dict):
        content = await self.get_content(elem)

        if content:
            href, pdf_pages, meta = content

            # TODO write meta information into context
            fields['pdf_url'] = href
            fields['pdf_pages'] = pdf_pages

    async def get_content(self, elem):
        href_property = await elem.getProperty('href')
        href = await href_property.jsonValue()

        file_path = await self.download(href)
        suffix = pathlib.Path(file_path).suffix

        # TODO currently only supports pdf files
        if suffix != '.pdf':
            return None

        pdf_pages, meta = self.get_meta(file_path)

        if os.path.exists(file_path):
            os.remove(file_path)

        return href, pdf_pages, meta

    async def download(self, url: str) -> str:
        download_path = self.context.download_path
        file_name = os.path.basename(urlparse(url).path)

        async with open_page(self.context.browser) as page:
            cdp = await page.target.createCDPSession()

            await cdp.send(
                'Page.setDownloadBehavior',
                {'behavior': 'allow', 'downloadPath': download_path},
            )

            download_promise = asyncio.ensure_future(page.waitForResponse(lambda res: res.url == url))
            await page.evaluate(DOWNLOAD_TEMPLATE % (url, file_name))
            await download_promise

        file_path = os.path.join(download_path, file_name)

        try:
            # chrome does some post-processing with the downloaded file even when the download finished
            # we wait for up to 10 seconds periodically checking if the file exists
            await asyncio.wait_for(self.wait_for_file(file_path), timeout=10)
        except asyncio.TimeoutError:
            raise ResolverError(_('Timeout waiting for download of %(url)s') % {'url': url})

        return file_path

    @staticmethod
    async def wait_for_file(path):
        while not os.path.isfile(path):
            await asyncio.sleep(1)

        return path

    @staticmethod
    def get_meta(path):
        try:
            pdf = pikepdf.open(path)
        except pikepdf.PdfError as err:
            raise ResolverError(_('Failed to open pdf: %(error)s') % {'error': str(err)})

        page_count = len(pdf.pages)
        meta = pdf.docinfo.as_dict()
        pdf.close()

        return page_count, meta


class StaticResolver(Resolver):
    def __init__(self, context: ScraperContext, *, key: str, value: str, **kwargs):
        super().__init__(context, **kwargs)
        self.key = key
        self.value = value

    async def resolve(self, node: ElementHandle, fields: dict, errors: dict):
        fields[self.key] = self.value


# FIXME
#  temporary solution that passed empty values to unused required kwargs
#  this should be better solved by splitting the selection and storage under a key into
#  dedicated resolvers that can be composed to show the intended behavior
class TagResolver(SelectorMixin, Resolver):
    def __init__(self, context: ScraperContext, *args, resolver: dict, **kwargs):
        super().__init__(context, *args, selector='', **kwargs)
        self.resolver = self.create_resolver(context, key='tag', **resolver)

    @staticmethod
    def create_resolver(context, *, type, **config):
        return ResolverType[type].create(context, **config)

    async def resolve(self, node: ElementHandle, fields: dict, errors: dict):
        tags = {}

        await self.resolver.resolve(node, tags, errors)

        fields.setdefault('tags', []).extend(tags.values())


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

    def create(self, context: dict, **config):
        return self.value(context, **config)
