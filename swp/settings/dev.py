from .base import *

from cosmogo.utils.settings import debug_toolbar, django_extensions

ENVIRONMENT = 'develop'

DEBUG = True

SECRET_KEY = 'this-is-not-a-secret-key'

ALLOWED_HOSTS = '*'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

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
