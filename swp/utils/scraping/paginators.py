import asyncio
from asyncio import Queue
from enum import Enum
from typing import Iterator

from playwright.async_api import ElementHandle, TimeoutError

from django.utils.translation import gettext_lazy as _

from swp.utils.scraping.context import ScraperContext
from swp.utils.scraping.exceptions import ResolverError
from swp.utils.scraping.resolvers.base import get_content

ENDLESS_PAGINATION_OBSERVER_TEMPLATE = """
    () => {
        const listElem = document.querySelector('%s');
        const observer = new MutationObserver(mutationList => {
            mutationList.forEach(mutation => {
                const nodes = Array.from(mutation.target.children);
                const addedNodes = Array.from(mutation.addedNodes);
                const indexes = addedNodes.map(node => nodes.indexOf(node));
                window.scraperHandleMutation(indexes);
            });
        });
        observer.observe(listElem, {childList: true});
    }
"""


class Paginator:

    def __init__(self, context: ScraperContext, *, list_selector: str, button_selector: str, item_selector: str = None,
                 max_pages: int = 10,
                 max_per_page: int = None,
                 timeout: int = 5):
        self.context = context
        self.list_selector = list_selector
        self.item_selector = item_selector or '*'
        self.selector = f'{self.list_selector} {self.item_selector}'
        self.button_selector = button_selector
        self.max_pages = max_pages
        self.max_per_page = max_per_page
        self.timeout = timeout

    async def query_list_items(self, page=None) -> [ElementHandle]:
        page = page or self.context.page

        nodes = await page.query_selector_all(self.selector)

        if not nodes:
            raise ResolverError(
                _('No elements matching %(selector)s found') % {'selector': self.selector}
            )

        return nodes[:self.max_per_page] if self.max_per_page else nodes


class EndlessPaginator(Paginator):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = Queue()

    async def get_nodes(self) -> Iterator[ElementHandle]:

        nodes = await self.query_list_items()

        for node in nodes:
            yield node

        await self.register_mutation_observer()

        for _ in range(self.max_pages):
            button = await self.context.page.query_selector(self.button_selector)

            if not button:
                return

            await button.click()

            try:
                indexes = await asyncio.wait_for(self.queue.get(), timeout=self.timeout)
            except asyncio.TimeoutError:
                return

            nodes = await self.query_list_items()

            for idx in indexes:
                yield nodes[idx]

            self.queue.task_done()

    def handle_mutation(self, indexes: [int]):
        self.queue.put_nowait(indexes)

    async def register_mutation_observer(self):
        await self.context.page.expose_function('scraperHandleMutation', self.handle_mutation)
        await self.context.page.evaluate(ENDLESS_PAGINATION_OBSERVER_TEMPLATE % self.list_selector)


class PagePaginator(Paginator):

    async def get_next_page(self) -> Iterator[ElementHandle]:
        nodes = await self.query_list_items()

        if not nodes:
            raise ResolverError(
                _('No elements matching %(selector)s found') % {'selector': self.selector}
            )

        yield nodes

        for page_number in range(self.max_pages - 1):
            next_page_link = await self.context.page.query_selector(self.button_selector)

            if not next_page_link:
                break

            href = await get_content(next_page_link, attr='href')

            if not href:
                raise ResolverError(
                    _('Pagination Button matching %(selector)s has no attribute href') % {
                        'selector': self.button_selector
                    }
                )

            await self.nagigate_to_next_page(href, page_number)

            nodes = await self.query_list_items()
            yield nodes

    async def nagigate_to_next_page(self, href, page_number):
        try:
            await self.context.page.goto(href)
        except TimeoutError:
            raise ResolverError(
                _('Timeout while navigating to page %(page_number)s: %(href)s') % {
                    'page_number': page_number,
                    'href': href,
                }
            )


class PaginatorType(Enum):
    Endless = EndlessPaginator
    Page = PagePaginator

    def create(self, context, **config):
        return self.value(context, **config)
