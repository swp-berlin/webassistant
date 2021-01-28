from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class AdminSite(admin.AdminSite):
    site_title = site_header = _('SWP Administration')
    index_title = _('Overview')
    enable_nav_sidebar = False

    def has_permission(self, request) -> bool:
        # [SWP-61] Restrict admin site access to superusers only
        return super().has_permission(request) and request.user.is_superuser
