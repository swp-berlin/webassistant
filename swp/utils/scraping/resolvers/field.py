from swp.utils.scraping.resolvers.base import Resolver, create_resolver


class FieldResolver(Resolver):
    key: str = None
    multiple: bool = False

    def __init__(self, context, *, resolver: dict):
        super(FieldResolver, self).__init__(context)
        config = {**resolver, 'key': self.key, 'multiple': self.multiple}
        self.resolver: Resolver = create_resolver(context, **config)

    async def resolve(self, *args, **kwargs):
        return await self.resolver.resolve(*args, **kwargs)
