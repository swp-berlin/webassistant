import asyncio
from asyncio import Queue

from django.utils.translation import gettext_lazy as _

from playwright.async_api import ElementHandle

from ..exceptions import ResolverError
from ..paginators import PaginatorType
from .base import IntermediateResolver


class ListResolver(IntermediateResolver):
    """
    Resolves every node selected by the given :selector by calling every resolver in the :resolvers list
    """

    def __init__(self, context, *args, selector: str, paginator: dict = None,
                 **kwargs):
        super().__init__(context, *args, **kwargs)

        if paginator:
            self.paginator = self.create_paginator(context, item_selector=selector, **paginator)
            self.selector = f'{paginator["list_selector"]} {selector}'
        else:
            self.selector = selector

    @staticmethod
    def create_paginator(context, *, type, **paginator):
        return PaginatorType[type].create(context, **paginator)

    async def worker(self, nodes: Queue, results: Queue):
        while True:
            node = await nodes.get()
            try:
                resolved = await self.resolve_node(node)
                results.put_nowait(resolved)
            except Exception as error:
                results.put_nowait(error)
            finally:
                nodes.task_done()

    async def process_nodes(self, nodes: Queue, results: Queue):
        workers = [asyncio.create_task(self.worker(nodes, results)) for _ in range(4)]

        async for node in self.resolve_nodes():
            nodes.put_nowait(node)

        await nodes.join()

        for worker in workers:
            worker.cancel()

        await asyncio.gather(*workers, return_exceptions=True)

        results.put_nowait(None)

    async def resolve(self) -> [dict]:
        nodes = Queue()
        results = Queue()

        asyncio.create_task(self.process_nodes(nodes, results))

        while True:
            result = await results.get()

            if result:
                if isinstance(result, Exception):
                    raise result

                yield result
            else:
                break

    async def resolve_nodes(self):
        if self.paginator:
            async for node in self.paginator.get_nodes():
                yield node
        else:
            nodes = await self.context.page.query_selector_all(self.selector)

            if not nodes:
                raise ResolverError(
                    _('No elements matching %(selector)s found') % {'selector': self.selector}
                )

            for node in nodes:
                yield node

    async def resolve_node(self, node: ElementHandle):
        fields = {}
        errors = {}

        for resolver in self.resolvers:
            await resolver.resolve(node, fields, errors)

        return {'fields': fields, 'errors': errors}
