from django.utils.translation import gettext_lazy as _

from ..exceptions import ResolverError
from .base import get_content
from .data import DataResolver


class AttributeResolver(DataResolver):

    def __init__(self, *args, attribute, **kwargs):
        super().__init__(*args, **kwargs)
        self.attribute = attribute

    async def get_single_content(self, element):
        value = await get_content(element, self.attribute)

        if not value:
            raise ResolverError(
                _('[Attribute Resolver] Element matching %(selector)s has no attribute %(attribute)s') % {
                    'selector': self.selector,
                    'attribute': self.attribute
                }
            )

        return await get_content(element, self.attribute)
