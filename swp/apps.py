from django.apps import AppConfig
from django.contrib.admin import apps


class SWPConfig(AppConfig):
    name = 'swp'
    verbose_name = 'SWP'
    default_auto_field = 'django.db.models.AutoField'
    default = True


class AdminConfig(apps.AdminConfig):
    default_site = 'swp.site.AdminSite'
    default = False
