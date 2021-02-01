from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic.detail import BaseDetailView

from swp.models import Thinktank
from swp.utils.ris import write_ris_data


class ThinkTankRISDownloadView(LoginRequiredMixin, BaseDetailView):
    queryset = Thinktank.objects.prefetch_related('publications')

    def render_to_response(self, context):
        thinktank: Thinktank = self.object

        response = HttpResponse(content_type='text/plain; charset=utf-8')
        response['Content-Disposition'] = f'inline; filename="{thinktank.name}.ris"'

        write_ris_data(response, *thinktank.publications.all())

        return response
