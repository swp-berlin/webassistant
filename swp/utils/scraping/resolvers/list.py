import asyncio
from asyncio import Queue

from playwright.async_api import ElementHandle

from ..paginators import PaginatorType
from .base import IntermediateResolver


class ListResolver(IntermediateResolver):
    """
    Resolves every node selected by the given :selector by calling every resolver in the :resolvers list
    """

    def __init__(self, context, *args, selector: str, paginator: dict = None,
                 **kwargs):
        super().__init__(context, *args, **kwargs)

        self.paginator = self.create_paginator(context, item_selector=selector, **paginator)

    @staticmethod
    def create_paginator(context, *, type: str = 'Page', **paginator):
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
        try:
            workers = [asyncio.create_task(self.worker(nodes, results)) for _ in range(4)]

            async for page in self.paginator.get_next_page():
                for node in page:
                    nodes.put_nowait(node)

                await nodes.join()

            for worker in workers:
                worker.cancel()

            await asyncio.gather(*workers, return_exceptions=True)
        finally:
            results.put_nowait(None)

    async def resolve(self) -> [dict]:
        nodes = Queue()
        results = Queue()

        process = asyncio.create_task(self.process_nodes(nodes, results))

        while True:
            result = await results.get()

            if result:
                if isinstance(result, Exception):
                    raise result

                yield result
            else:
                break

        await process

        if process.exception():
            raise process.exception()

    async def resolve_node(self, node: ElementHandle):
        fields = {}
        errors = {}

        for resolver in self.resolvers:
            await resolver.resolve(node, fields, errors)

        return {'fields': fields, 'errors': errors}
