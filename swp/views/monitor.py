from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic.detail import BaseDetailView

from swp.models import Monitor
from swp.utils.ris import write_ris_data, RIS_MEDIA_TYPE


class MonitorRISDownloadView(LoginRequiredMixin, BaseDetailView):
    exclude_sent = False
    queryset = Monitor.objects.all()

    def render_to_response(self, context):
        monitor: Monitor = self.object

        response = HttpResponse(content_type=RIS_MEDIA_TYPE)
        response['Content-Disposition'] = f'attachment; filename="{monitor.name}.ris"'

        write_ris_data(response, *monitor.get_publications(exclude_sent=self.exclude_sent))

        return response
