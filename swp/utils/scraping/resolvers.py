import asyncio
import os
import pathlib
from enum import Enum
from urllib.parse import urlparse

import pikepdf
from pyppeteer.element_handle import ElementHandle

from .context import ScraperContext
from .exceptions import DocumentDownloadError, NodeNotFoundError, SkippedError
from .paginators import PaginatorType
from .selectors import Selector


class Resolver:

    def __init__(self, context: ScraperContext, *, selector: Selector, **kwargs):
        self.context = context
        self.selector = selector


class IntermediateResolver(Resolver):

    def __init__(self, context: ScraperContext, *args, resolvers: [dict], **kwargs):
        super().__init__(context, *args, **kwargs)
        self.resolvers = [self.create_resolver(context, **config) for config in resolvers]

    @staticmethod
    def create_resolver(context, *, type, **config):
        return ResolverType[type].create(context, **config)


class ListResolver(IntermediateResolver):
    """
    Resolves every node selected by the given :selector by calling every resolver in the :resolvers list
    """

    def __init__(self, context, *args, paginator: dict = None, **kwargs):
        super().__init__(context, *args, **kwargs)

        if paginator:
            self.paginator = self.create_paginator(context, **paginator)

    @staticmethod
    def create_paginator(context, *, type, **paginator):
        return PaginatorType[type].create(context, **paginator)

    async def resolve(self) -> [dict]:
        async for node in self.resolve_nodes():
            try:
                detail_context = await self.resolve_node(node)
            except SkippedError:
                continue

            yield detail_context

    async def resolve_nodes(self):
        if self.paginator:
            async for node in self.paginator.get_nodes():
                yield node
        else:
            nodes = await self.context.page.querySelectorAll(self.selector)

            for node in nodes:
                yield node

    async def resolve_node(self, node: ElementHandle):
        context = {}

        for resolver in self.resolvers:
            await resolver.resolve(node, context)

        print(context)

        return context


class LinkResolver(IntermediateResolver):

    def __init__(self, *args, same_site: bool = False, **kwargs):
        super().__init__(*args, **kwargs)
        self.same_site = same_site

    async def get_href(self, node: ElementHandle) -> str:
        elem = await node.querySelector(self.selector)

        href_property = await elem.getProperty('href')
        # noinspection PyTypeChecker
        href: str = await href_property.jsonValue()

        if self.same_site:
            url = self.context.page.url

            if urlparse(href).netloc != urlparse(url).netloc:
                raise SkippedError

        return href

    async def resolve(self, node: ElementHandle, context: dict):
        href = await self.get_href(node)

        detail_page = await self.context.browser.newPage()
        await detail_page.goto(href)

        for resolver in self.resolvers:
            await resolver.resolve(detail_page, context)

        await detail_page.close()


class DataResolver(Resolver):

    def __init__(self, *args, key: str, required: bool = True, **kwargs):
        super().__init__(*args, **kwargs)
        self.required = required
        self.key = key

    async def resolve(self, node: ElementHandle, context: dict):
        elem = await node.querySelector(self.selector)

        if not elem:
            if self.required:
                raise NodeNotFoundError
            else:
                return

        await self.handle_element(elem, context)

    async def handle_element(self, elem: ElementHandle, context: dict):
        text = await self.get_content(elem)

        context[self.key] = text

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

    async def handle_element(self, elem: ElementHandle, context: dict):
        content = await self.get_content(elem)

        if content:
            href, pdf_pages, meta = content

            # TODO write meta information into context
            context['pdf_url'] = href
            context['pdf_pages'] = pdf_pages

    async def get_content(self, elem):
        href_property = await elem.getProperty('href')
        href = await href_property.jsonValue()

        try:
            file_path = await self.download(href)
        except DocumentDownloadError:
            return None

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

        page = await self.context.browser.newPage()
        cdp = await page.target.createCDPSession()

        await cdp.send(
            'Page.setDownloadBehavior',
            {'behavior': 'allow', 'downloadPath': download_path},
        )

        download_promise = asyncio.ensure_future(page.waitForResponse(lambda res: res.url == url))
        await page.evaluate(DOWNLOAD_TEMPLATE % (url, file_name))
        await download_promise

        await page.close()

        file_path = os.path.join(download_path, file_name)

        try:
            # chrome does some post-processing with the downloaded file even when the download finished
            # we wait for up to 10 seconds periodically checking if the file exists
            await asyncio.wait_for(self.wait_for_file(file_path), timeout=10)
        except asyncio.TimeoutError:
            raise DocumentDownloadError

        return file_path

    @staticmethod
    async def wait_for_file(path):
        while not os.path.isfile(path):
            await asyncio.sleep(1)

        return path

    @staticmethod
    def get_meta(path):
        pdf = pikepdf.open(path)
        page_count = len(pdf.pages)
        meta = pdf.docinfo.as_dict()
        pdf.close()

        return page_count, meta


class StaticResolver:
    def __init__(self, context: ScraperContext, *, key: str, value: str):
        self.context = context
        self.key = key
        self.value = value

    async def resolve(self, node: ElementHandle, context: dict):
        context[self.key] = self.value


# FIXME
#  temporary solution that passed empty values to unused required kwargs
#  this should be better solved by splitting the selection and storage under a key into
#  dedicated resolvers that can be composed to show the intended behavior

class TagsResolver(IntermediateResolver):
    def __init__(self, context: ScraperContext, *args, resolvers: [dict], **kwargs):
        super().__init__(context, *args, selector='', **kwargs)
        self.resolvers = [self.create_resolver(context, key=str(i), **config) for i, config in enumerate(resolvers)]

    async def resolve(self, node: ElementHandle, context: dict):
        tags = {}

        for resolver in self.resolvers:
            await resolver.resolve(node, tags)

        context.setdefault('tags', []).extend(tags.values())


class ResolverType(Enum):
    List = ListResolver
    Link = LinkResolver
    Data = DataResolver
    Attribute = AttributeResolver
    Document = DocumentResolver
    Static = StaticResolver
    Tags = TagsResolver
    TagsData = Data
    TagsAttribute = Attribute
    TagsStatic = Static

    def create(self, context: dict, **config):
        return self.value(context, **config)
