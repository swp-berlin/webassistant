from distutils.spawn import find_executable

from .base import *

from swp.utils.settings import env, debug_toolbar, django_extensions

ENVIRONMENT = 'develop'

DEBUG = True

SECRET_KEY = 'this-is-not-a-secret-key'

ALLOWED_HOSTS = ['*']

if find_executable('mailhog'):
    EMAIL_PORT = 1025
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

REST_FRAMEWORK_DEFAULT_RENDERER_CLASSES.append('rest_framework.renderers.BrowsableAPIRenderer')

[
    INSTALLED_APPS,
    MIDDLEWARE,
    INTERNAL_IPS,
    DEBUG_TOOLBAR,
    DEBUG_TOOLBAR_CONFIG,
] = debug_toolbar(
    INSTALLED_APPS,
    MIDDLEWARE,
)

INSTALLED_APPS = django_extensions(INSTALLED_APPS)

AUTH_PASSWORD_VALIDATORS = []
