from __future__ import annotations

import asyncio
from collections import defaultdict
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from playwright.async_api import Browser, Page


@dataclass
class ScraperContext:
    browser: Browser
    page: Page
    locks: defaultdict = field(default_factory=lambda: defaultdict(asyncio.Lock))
    stopped: bool = False

    def lock(self, name):
        return self.locks[name]
