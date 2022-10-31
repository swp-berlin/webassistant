from swp.utils.settings import configure_sentry

from .base import *

ENVIRONMENT = env('ENVIRONMENT', 'staging')

configure_sentry(
    'https://3710c408a1494bc6b43038ed20acfed5@sentry.cosmocode.de/48',
    ENVIRONMENT,
    RELEASE,
    celery=True,
    send_default_pii=True,
)

ALLOWED_HOSTS = ['staging.swp.cosmoco.de', 'staging.swp.cosmocode.de']

DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', 'staging@swp.cosmocode.de')

USE_X_FORWARDED_FOR = True
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SITE_ID = 2
