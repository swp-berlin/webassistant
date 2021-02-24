import json
import os
from contextlib import asynccontextmanager, contextmanager
from typing import ContextManager

from playwright.async_api import async_playwright, Browser, Page

from cosmogo.utils.tempdir import maketempdir

PAGE_WAIT_UNTIL = 'networkidle'


DEFAULT_PREFERENCES = {
    'plugins': {
        'always_open_pdf_externally': True,
    }
}


@contextmanager
def tempoary_user_dir():
    with maketempdir() as temp_dir:
        pref_file_path = temp_dir / 'Default' / 'Preferences'

        os.makedirs(os.path.dirname(pref_file_path), exist_ok=True)

        with open(pref_file_path, 'w') as pref_file:
            json.dump(DEFAULT_PREFERENCES, pref_file)

        yield temp_dir


@asynccontextmanager
async def open_browser(*args, **kwargs) -> ContextManager[Browser]:
    kwargs.setdefault('accept_downloads', True)

    if kwargs.pop('debug', False):
        kwargs.setdefault('headless', False)
        kwargs.setdefault('slow_mo', 100)
        kwargs.setdefault('devtools', True)

    async with async_playwright() as playwright:
        with tempoary_user_dir() as user_dir:
            browser = await playwright.chromium.launch_persistent_context(user_dir, *args, **kwargs)

        try:
            yield browser
        finally:
            await browser.close()


@asynccontextmanager
async def open_page(browser: Browser, *args, **kwargs) -> ContextManager[Page]:
    page = await browser.new_page(*args, **kwargs)

    try:
        yield page
    finally:
        await page.close()
