import json
import os
from contextlib import asynccontextmanager, contextmanager
from typing import ContextManager

from playwright.async_api import async_playwright, Browser, Page

from django.conf import settings
from cosmogo.utils.tempdir import maketempdir


DEFAULT_PREFERENCES = {
    'plugins': {
        'always_open_pdf_externally': True,
    }
}

DEFAULT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'


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

    if kwargs.pop('debug', settings.PLAYWRIGHT_DEBUG):
        kwargs.setdefault('headless', False)
        kwargs.setdefault('slow_mo', 100)
        kwargs.setdefault('devtools', True)

    async with async_playwright() as playwright:
        with tempoary_user_dir() as user_dir:
            browser = await playwright.chromium.launch_persistent_context(
                user_dir,
                *args,
                user_agent=DEFAULT_USER_AGENT,
                **kwargs
            )

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
