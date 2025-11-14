from django.views.generic import TemplateView

from swp.api.v1.router import default_router

__all__ = [
    'OpenAPIExplorerView',
]


@default_router.register('explorer')
class OpenAPIExplorerView(TemplateView):
    template_name = 'api/explorer.html'
