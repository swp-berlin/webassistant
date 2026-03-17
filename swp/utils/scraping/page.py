from typing import Optional

from playwright.async_api import Page, Response

RESPONSE = 'current-response'


def get_response(page: Page) -> Optional[Response]:
    return getattr(page, RESPONSE, None)


def set_response(page: Page, response: Response = None):
    setattr(page, RESPONSE, response)


def get_status(page: Page):
    response = get_response(page)

    if response is None:
        return 0

    return response.status


async def goto(page: Page, url: str, **kwargs) -> Optional[Response]:
    response = await page.goto(url, **kwargs)

    set_response(page, response)

    return response
