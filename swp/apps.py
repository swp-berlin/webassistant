from django.apps import AppConfig


class SWPConfig(AppConfig):
    name = 'swp'
    verbose_name = 'SWP'

    def ready(self):
        from swp import checks
