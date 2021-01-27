from contextlib import asynccontextmanager, contextmanager
from dataclasses import dataclass
from datetime import datetime

from pyppeteer import launch

from cosmogo.utils.tempdir import maketempdir
from .browser import open_browser, open_page
from .context import ScraperContext
from .resolvers import ResolverType


URL = str


@dataclass
class Publication:
    title: str
    author: str = None
    published_on: datetime = None

    @property
    def hash(self) -> str:
        # TODO
        return ''


@dataclass
class WatchTarget:
    url: URL
    resolver_config: dict

    async def scrape(self) -> [Publication]:
        scraper = Scraper(self.url)

        scraped = await scraper.scrape(self.resolver_config)

        # TODO
        return [Publication(**context) for context in scraped]


class Scraper:

    def __init__(self, url: URL, *, download_path: str = None):
        self.url = url
        self.download_path = download_path

    async def scrape(self, resolver_config: dict) -> [dict]:
        async with open_browser(handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False) as browser:
            async with open_page(browser) as page:
                await page.goto(self.url)

                with self.get_download_path() as download_path:
                    context = ScraperContext(browser, page, download_path)
                    resolver = self.get_resolver(context, **resolver_config)

                    async for resolved in resolver.resolve():
                        yield resolved

    @contextmanager
    def get_download_path(self):
        if self.download_path:
            yield self.download_path
            return

        with maketempdir() as download_path:
            yield f'{download_path}'

    def get_resolver(self, context, *, type: ResolverType, **config):
        return ResolverType[type].create(context, **config)
