from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .mixins import UserDataMixin


class SWPView(LoginRequiredMixin, UserDataMixin, TemplateView):
    template_name = 'swp.html'
