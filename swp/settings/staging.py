from cosmogo.utils.settings import configure_sentry

from .base import *

ENVIRONMENT = env('ENVIRONMENT', 'staging')

configure_sentry('https://3710c408a1494bc6b43038ed20acfed5@sentry.cosmocode.de/48', ENVIRONMENT, RELEASE)

ALLOWED_HOSTS = ['staging.swp.cosmoco.de', 'staging.swp.cosmocode.de']

USE_X_FORWARDED_FOR = True
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')