from typing import List, Optional, Union

from django.utils.translation import gettext_lazy as _

from playwright.async_api import ElementHandle, TimeoutError

from ..exceptions import ErrorLevel, ResolverError
from ..utils import get_error
from .base import Resolver, SelectorMixin, get_content


class DataResolver(SelectorMixin, Resolver):

    def __init__(self, *args, key: str, required: bool = False, ignore_empty: bool = False, **kwargs):
        super().__init__(*args, **kwargs)

        self.required = required
        self.key = key
        self.ignore_empty = ignore_empty

    async def get_element(self, node: ElementHandle) -> Union[Optional[ElementHandle], List[ElementHandle]]:
        try:
            # [SWP-144] Precautionary measure against dynamically loaded nodes
            await node.wait_for_selector(self.selector, state='attached', timeout=5000)
        except TimeoutError as exc:
            raise self.make_error(
                _('No element matches %(selector)s') % {'selector': self.selector},
            ) from exc

        return await super().get_element(node)

    async def resolve(self, node: ElementHandle, fields: dict, errors: dict):
        try:
            await self._resolve(node, fields, errors)
        except ResolverError as err:
            errors[self.key] = get_error(err)

    async def _resolve(self, node: ElementHandle, fields: dict, errors: dict):
        elem = await self.get_element(node)

        if not elem:
            raise ResolverError(
                _('No element matches %(selector)s') % {'selector': self.selector},
                level=ErrorLevel.ERROR if self.required else ErrorLevel.WARNING
            )

        await self.handle_element(elem, fields)

    async def handle_element(self, elem: ElementHandle, fields: dict):
        text = await self.get_content(elem)

        fields[self.key] = text

    async def get_content(self, elem):
        if self.multiple:
            return await self.get_multiple_content(elem)

        return await self.get_single_content(elem)

    async def get_single_content(self, element):
        return await get_content(element)

    async def get_multiple_content(self, elements):
        texts = set()

        for elem in elements:
            text = await self.get_single_content(elem)
            if not text and self.ignore_empty:
                continue

            texts.add(text)

        return list(texts)
