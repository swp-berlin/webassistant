from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import BaseDetailView

from swp.models import Monitor, ThinktankFilter
from swp.utils.ris import RISResponse


class MonitorRISDownloadView(LoginRequiredMixin, BaseDetailView):
    exclude_sent = False
    queryset = Monitor.objects.all()

    def render_to_response(self, context):
        monitor: Monitor = self.object
        publications = monitor.get_publications(exclude_sent=self.exclude_sent)

        return RISResponse(publications, filename=f'{monitor.name}.ris')


class ThinktankFilterRISDownloadView(LoginRequiredMixin, BaseDetailView):
    exclude_sent = False
    queryset = ThinktankFilter.objects.select_related('monitor')

    def render_to_response(self, context):
        monitor: Monitor = self.object.monitor

        publications = monitor.get_publications(exclude_sent=self.exclude_sent, filter_by=self.object)

        return RISResponse(publications, filename=f'{monitor.name}.ris')
