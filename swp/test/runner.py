import os
import shutil

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test.runner import DiscoverRunner


class CosmoCodeTestRunner(DiscoverRunner):

    def setup_test_environment(self, **kwargs):
        if settings.MEDIA_ROOT == settings.BASE_DIR / 'media':  # pragma: no cover
            raise ImproperlyConfigured(
                f'Make sure to set MEDIA_ROOT to a directory distinct from the '
                f'default MEDIA_ROOT when using {self.__class__.__name__}'
            )

        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        DiscoverRunner.setup_test_environment(self, **kwargs)

    def teardown_test_environment(self, **kwargs):
        DiscoverRunner.teardown_test_environment(self, **kwargs)
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
