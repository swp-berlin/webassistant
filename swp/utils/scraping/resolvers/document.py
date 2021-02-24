import pathlib
from typing import Optional

import pikepdf

from django.utils.translation import gettext_lazy as _

from playwright.async_api import ElementHandle, Error as PlaywrightError, Page, TimeoutError

from swp.utils.scraping.exceptions import ResolverError
from swp.utils.scraping.resolvers.data import DataResolver


class DocumentResolver(DataResolver):

    async def resolve(self, page: Page, fields: dict, errors: dict):
        elem = await self.get_element(page)

        try:
            async with page.expect_download() as download_info:
                await elem.click()
        except TimeoutError:
            raise ResolverError(_('Timeout while trying to download the document at %(url)s' % {'url': page.url}))

        download = await download_info.value
        file_path = await download.path()
        suffix = pathlib.Path(file_path).suffix.lower()

        # TODO currently only supports pdf files
        if suffix != '.pdf':
            return None

        pdf_pages, meta = self.get_meta(file_path)

        fields['pdf_url'] = download.url
        fields['pdf_pages'] = pdf_pages

    async def get_element(self, page: Page) -> Optional[ElementHandle]:
        try:
            [elem, *other] = await page.query_selector_all(self.selector)
        except PlaywrightError as err:
            raise ResolverError(str(err))

        if other:
            raise ResolverError(_('%(selector)s matches more than one document.') % {'selector': self.selector})

        return elem

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
