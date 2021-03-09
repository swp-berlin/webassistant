from django.http import FileResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_control
from django.views.decorators.http import last_modified

from swp.utils.snippets import get_template
from swp.utils.translation import get_language

LAST_MODIFIED = timezone.now()


@method_decorator(cache_control(public=True, max_age=60 * 5, must_revalidate=True), name='get')
@method_decorator(last_modified(lambda *args, **kwargs: LAST_MODIFIED), name='get')
class SnippetView(View):

    def get(self, request, identifier):
        language = get_language(request=self.request)
        template = get_template(identifier, language)

        return FileResponse(
            open(template.origin.name, 'rb'),
            content_type='text/markdown',
            charset='utf-8',
        )
