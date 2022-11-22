from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import BaseDetailView

from swp.models import Thinktank
from swp.utils.ris import RISResponse


class ThinkTankRISDownloadView(LoginRequiredMixin, BaseDetailView):
    queryset = Thinktank.objects.prefetch_related('publications')

    def render_to_response(self, context):
        thinktank: Thinktank = self.object
        publications = thinktank.publications.all()

        return RISResponse(publications, filename=f'{thinktank.name}.ris')
