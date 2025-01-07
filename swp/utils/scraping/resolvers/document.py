from typing import Optional, Union

import pikepdf

from django.utils.translation import gettext_lazy as _

from playwright.async_api import ElementHandle, Page, TimeoutError

from swp.utils.scraping.resolvers.data import DataResolver


class DocumentResolver(DataResolver):

    def __init__(self, *args, key: str = None, required: bool = False, **kwargs):
        kwargs['key'] = key or 'document'
        kwargs['multiple'] = True
        kwargs['required'] = required

        super().__init__(*args, **kwargs)

    async def _resolve(self, node: Union[Page, ElementHandle], fields: dict, errors: dict):
        page: Page = node if isinstance(node, Page) else self.context.page
        elem = await self.get_element(node)

        if not elem:
            raise self.make_error(_('No document for selector %(selector)s found.') % {'selector': self.selector})

        # [SWP-137] Playwright does not handle downloads in new tabs (#1967)
        await elem.evaluate('node => node.removeAttribute("target")')

        async with self.context.lock('download'):
            try:
                async with page.expect_download() as download_info:
                    # we dispatch a programmatic click, not an emulated mouse click because
                    # we also want elements to be clicked that are not visible (e.g. width of 0 or display: none)
                    await elem.dispatch_event("click")
            except TimeoutError:
                raise self.make_error(
                    _('Timeout while trying to download the document at %(url)s' % {'url': page.url})
                )

        download = await download_info.value
        file_path = await download.path()

        pdf_pages = self.get_pdf_pages(file_path)

        fields['pdf_url'] = download.url
        fields['pdf_pages'] = pdf_pages
        fields['pdf_path'] = file_path

    async def get_element(self, node: ElementHandle) -> Optional[ElementHandle]:
        elements = await super().get_element(node)

        if len(elements) > 1:
            raise self.make_error(_('%(selector)s matches more than one document.') % {'selector': self.selector})

        return elements[0] if elements else None

    def get_pdf_pages(self, path) -> int:
        try:
            with pikepdf.open(path) as pdf:
                return len(pdf.pages)
        except pikepdf.PdfError as error:
            raise self.make_error(_('Failed to open pdf: %(error)s') % {'error': error})
