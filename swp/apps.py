from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig as DefaultAdminConfig


class SWPConfig(AppConfig):
    name = 'swp'
    verbose_name = 'SWP'
    default_auto_field = 'django.db.models.AutoField'


class AdminConfig(DefaultAdminConfig):
    default_site = 'swp.site.AdminSite'
    default = False
