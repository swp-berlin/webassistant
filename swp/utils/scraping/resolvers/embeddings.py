from swp.utils.scraping.resolvers.base import get_content
from swp.utils.scraping.resolvers.data import DataResolver


class EmbeddingsResolver(DataResolver):

    def __init__(self, *args, key: str = None, required: bool = False, **kwargs):
        kwargs['key'] = key or 'text_content'
        kwargs['multiple'] = False
        kwargs['ignore_empty'] = True
        kwargs['required'] = required

        super().__init__(*args, **kwargs)

    async def get_single_content(self, element):
        return await get_content(element, 'innerText')
