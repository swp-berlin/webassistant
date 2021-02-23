import asyncio
import os
import pathlib
from typing import Optional
from urllib.parse import urlparse

import pikepdf
from django.utils.translation import gettext_lazy as _

from pyppeteer.element_handle import ElementHandle
from pyppeteer.errors import ElementHandleError

from swp.utils.scraping.browser import open_page
from swp.utils.scraping.exceptions import ResolverError
from swp.utils.scraping.resolvers.data import DataResolver


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
