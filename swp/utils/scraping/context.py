from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from playwright.async_api import Browser, Page


@dataclass
class ScraperContext:
    browser: Browser
    page: Page
    stopped: bool = False
