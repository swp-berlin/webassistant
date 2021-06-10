from django.utils.translation import gettext_lazy as _
from playwright.async_api import ElementHandle

from ..exceptions import ResolverError
from .data import DataResolver


class AttributeResolver(DataResolver):

    def __init__(self, *args, attribute, **kwargs):
        super().__init__(*args, **kwargs)
        self.attribute = attribute

    async def get_single_content(self, element: ElementHandle):
        if self.attribute == 'href':
            href_property = await element.get_property(self.attribute)
            value = await href_property.json_value()
        else:
            value = await element.get_attribute(self.attribute)

        if not value:
            raise ResolverError(
                _('[Attribute Resolver] Element matching %(selector)s has no attribute %(attribute)s') % {
                    'selector': self.selector,
                    'attribute': self.attribute
                }
            )

        return value
