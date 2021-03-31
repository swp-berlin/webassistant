from playwright.async_api import ElementHandle

from swp.utils.scraping.resolvers.base import Resolver, create_resolver


class FieldResolver(Resolver):
    key: str = None
    multiple: bool = False
    normalize = None

    def __init__(self, context, *, resolver: dict):
        super(FieldResolver, self).__init__(context)
        config = {**resolver, 'key': self.key, 'multiple': self.multiple}

        self.resolver: Resolver = create_resolver(context, **config)

    async def resolve(self, node: ElementHandle, fields: dict, *args, **kwargs):
        await self.resolver.resolve(node, fields, *args, **kwargs)

        value = fields.get(self.key)
        if value and callable(self.normalize):
            value = self.normalize(value)
        fields[self.key] = value
