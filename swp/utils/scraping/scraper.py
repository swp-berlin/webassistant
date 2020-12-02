from dataclasses import dataclass
from datetime import datetime

from pyppeteer import launch

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

    def __init__(self, url: URL):
        self.url = url

    async def scrape(self, resolver_config: dict) -> [dict]:
        browser = await launch()
        page = await browser.newPage()
        await page.goto(self.url)

        resolver = self.get_resolver(ScraperContext(browser, page), **resolver_config)

        scraped = await resolver.resolve()

        await page.close()
        await browser.close()

        return scraped

    def get_resolver(self, context, *, type: ResolverType, **config):
        return ResolverType[type].create(context, **config)
