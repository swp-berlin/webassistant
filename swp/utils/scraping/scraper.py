from contextlib import contextmanager
from typing import AsyncGenerator, List, TypedDict

from pyppeteer.errors import PyppeteerError
from sentry_sdk import capture_exception

from cosmogo.utils.tempdir import maketempdir

from .browser import open_browser, open_page
from .context import ScraperContext
from .exceptions import ScraperError
from .resolvers import ResolverType


URL = str


class Error(TypedDict):
    message: str
    level: str


class Result(TypedDict):
    fields: dict
    errors: List[Error]


class Scraper:

    def __init__(self, url: URL, *, download_path: str = None):
        self.url = url
        self.download_path = download_path

    async def scrape(self, resolver_config: dict) -> AsyncGenerator[Result, None]:
        try:
            async with open_browser(handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False) as browser:
                async with open_page(browser) as page:
                    await page.goto(self.url)

                    with self.get_download_path() as download_path:
                        context = ScraperContext(browser, page, download_path)
                        resolver = self.get_resolver(context, **resolver_config)

                        async for result in resolver.resolve():
                            yield result
        except PyppeteerError as err:
            raise ScraperError(str(err)) from err
        except Exception as exc:
            capture_exception(exc)
            raise

    @contextmanager
    def get_download_path(self):
        if self.download_path:
            yield self.download_path
            return

        with maketempdir() as download_path:
            yield f'{download_path}'

    def get_resolver(self, context, *, type: ResolverType, **config):
        return ResolverType[type].create(context, **config)
