from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig as DefaultAdminConfig


class SWPConfig(AppConfig):
    name = 'swp'
    verbose_name = 'SWP'

    def ready(self):
        from swp import checks


class AdminConfig(DefaultAdminConfig):
    default_site = 'swp.site.AdminSite'
