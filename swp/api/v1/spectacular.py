from django.utils import translation

from drf_spectacular.utils import extend_schema
from drf_spectacular.views import SpectacularAPIView as BaseSpectacularAPIView

from swp.api.v1 import default_router

__all__ = [
    'SWPSpectacularAPIView',
]


@default_router.register('schema')
class SWPSpectacularAPIView(BaseSpectacularAPIView):

    @extend_schema(parameters=None)
    @translation.override('en')
    def get(self, request, *args, **kwargs):
        return BaseSpectacularAPIView.get(self, request, *args, **kwargs)
