from contextlib import asynccontextmanager
from typing import ContextManager

from pyppeteer import launch
from pyppeteer.browser import Browser
from pyppeteer.page import Page


PAGE_WAIT_UNTIL = [
    'domcontentloaded',  # Not strictly required, but seems sensible
    'load',  # Default event for page.goto
    'networkidle0',  # SWP-81 Required for dynamic pages
]


@asynccontextmanager
async def open_browser(*args, **kwargs) -> ContextManager[Browser]:
    browser = await launch(*args, **kwargs)

    try:
        yield browser
    finally:
        await browser.close()


@asynccontextmanager
async def open_page(browser: Browser) -> ContextManager[Page]:
    page = await browser.newPage()

    try:
        yield page
    finally:
        await page.close()
