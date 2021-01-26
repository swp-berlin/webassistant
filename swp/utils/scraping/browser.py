from contextlib import asynccontextmanager
from typing import ContextManager

from pyppeteer import launch
from pyppeteer.browser import Browser
from pyppeteer.page import Page


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
