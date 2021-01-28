from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class AdminSite(admin.AdminSite):
    site_title = site_header = _('SWP Administration')
    index_title = _('Overview')
    enable_nav_sidebar = False
