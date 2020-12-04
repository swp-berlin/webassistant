from dataclasses import dataclass

from pyppeteer.browser import Browser
from pyppeteer.page import Page


@dataclass
class ScraperContext:
    browser: Browser
    page: Page
    download_path: str
