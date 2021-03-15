from typing import Any, AsyncGenerator, Mapping, TypedDict

from playwright.async_api import Error as PlaywrightError
from sentry_sdk import capture_exception

from .browser import open_browser, open_page, PAGE_WAIT_UNTIL
from .context import ScraperContext
from .exceptions import ScraperError
from .resolvers.base import create_resolver


URL = str


class Error(TypedDict):
    message: str
    level: str


class Result(TypedDict):
    fields: dict
    errors: Mapping[str, Error]


class Scraper:

    def __init__(self, url: URL, *, download_path: str = None):
        self.url = url
        self.download_path = download_path

    async def scrape(self, resolver_config: Mapping[str, Any]) -> AsyncGenerator[Result, None]:
        try:
            async with open_browser() as browser:
                async with open_page(browser) as page:
                    await page.goto(self.url, wait_until=PAGE_WAIT_UNTIL)

                    context = ScraperContext(browser, page)
                    resolver = create_resolver(context, **resolver_config)

                    results = resolver.resolve()

                    async for result in results:
                        yield result

        except PlaywrightError as err:
            raise ScraperError(str(err)) from err
        except Exception as exc:
            capture_exception(exc)
            raise
