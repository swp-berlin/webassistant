import pathlib
from typing import Optional, Tuple, Union

import pikepdf

from django.utils.translation import gettext_lazy as _

from playwright.async_api import ElementHandle, Page, TimeoutError

from swp.utils.scraping.resolvers.data import DataResolver


class DocumentResolver(DataResolver):

    def __init__(self, *args, required: bool = False, **kwargs):
        safe_key = kwargs.pop('key', '') or 'document'
        super().__init__(*args, key=safe_key, required=required, multiple=True, **kwargs)

    async def _resolve(self, node: Union[Page, ElementHandle], fields: dict, errors: dict):
        page: Page = node if isinstance(node, Page) else self.context.page
        elem = await self.get_element(node)

        if not elem:
            raise self.make_error(_('No document for selector %(selector)s found.') % {'selector': self.selector})

        # [SWP-137] Playwright does not handle downloads in new tabs (#1967)
        await elem.evaluate('node => node.removeAttribute("target")')

        try:
            async with page.expect_download() as download_info:
                # we dispatch a programmatic click, not an emulated mouse click
                # because we also want elements to be clicked that are not visible (e.g. width of 0 or display: none)
                await elem.dispatch_event("click")
        except TimeoutError:
            raise self.make_error(_('Timeout while trying to download the document at %(url)s' % {'url': page.url}))

        download = await download_info.value
        file_path = await download.path()

        pdf_pages, meta = self.get_meta(file_path)

        fields['pdf_url'] = download.url
        fields['pdf_pages'] = pdf_pages

    async def get_element(self, node: ElementHandle) -> Optional[ElementHandle]:
        elements = await super().get_element(node)

        if len(elements) > 1:
            raise self.make_error(_('%(selector)s matches more than one document.') % {'selector': self.selector})

        return elements[0] if elements else None

    def get_meta(self, path) -> Tuple[int, dict]:
        try:
            pdf = pikepdf.open(path)
        except pikepdf.PdfError as err:
            raise self.make_error(_('Failed to open pdf: %(error)s') % {'error': str(err)})

        page_count = len(pdf.pages)
        meta = pdf.docinfo.as_dict()
        pdf.close()

        return page_count, meta
