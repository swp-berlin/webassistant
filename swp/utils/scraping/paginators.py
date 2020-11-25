import asyncio
from asyncio import Queue
from enum import Enum
from typing import Iterator

from pyppeteer.element_handle import ElementHandle

from swp.utils.scraping.context import ScraperContext


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
                 max_pages: int = 10, timeout: int = 5):
        self.context = context
        self.list_selector = list_selector
        self.item_selector = item_selector or '*'
        self.button_selector = button_selector
        self.max_pages = max_pages
        self.timeout = timeout

    async def query_list_items(self, page=None) -> [ElementHandle]:
        page = page or self.context.page

        nodes = await page.querySelectorAll(f'{self.list_selector} > {self.item_selector}')
        return nodes


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
            button = await self.context.page.querySelector(self.button_selector)

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
        await self.context.page.exposeFunction('scraperHandleMutation', self.handle_mutation)
        await self.context.page.evaluate(ENDLESS_PAGINATION_OBSERVER_TEMPLATE % self.list_selector)


class PagePaginator(Paginator):

    async def get_nodes(self) -> Iterator[ElementHandle]:
        nodes = await self.query_list_items()

        for node in nodes:
            yield node

        for _ in range(self.max_pages):
            next_page_link = await self.context.page.querySelector(self.button_selector)

            if not next_page_link:
                return

            href_property = await next_page_link.getProperty('href')
            # noinspection PyTypeChecker
            href: str = await href_property.jsonValue()

            page = await self.context.browser.newPage()
            await page.goto(href)

            nodes = await self.query_list_items(page)

            for node in nodes:
                yield node

            await page.close()


class PaginatorType(Enum):
    Endless = EndlessPaginator
    Page = PagePaginator

    def create(self, context, **config):
        return self.value(context, **config)
