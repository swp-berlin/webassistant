from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class SWPView(LoginRequiredMixin, TemplateView):
    template_name = 'swp.html'
