from django.conf import settings
from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.urls import path
from django.utils.translation import gettext_lazy as _

from swp.views.spooling import SpoolingView


class AdminSite(admin.AdminSite):
    site_title = site_header = _('SWP Administration')
    index_title = _('Overview')
    enable_nav_sidebar = False

    def get_urls(self):
        return [
            path('spooling/', self.admin_view(self.spooling_view), name='spooling'),
            path('spooling/<state>/<date:date>/<path:filename>', self.admin_view(self.spooling_view), name='spooling'),
            *admin.AdminSite.get_urls(self),
        ]

    def spooling_view(self, request, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied

        directory = settings.EMBEDDING_SPOOLING_DIR

        if kwargs:
            return SpoolingView.file_response(directory, **kwargs)

        view = SpoolingView.as_view(
            site=self,
            directory=directory,
            extra_context=self.each_context(request),
        )

        return view(request)
