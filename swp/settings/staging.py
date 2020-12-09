from .base import *

DEBUG = False

ALLOWED_HOSTS = ['staging.swp.cosmoco.de', 'staging.swp.cosmocode.de']

USE_X_FORWARDED_FOR = True
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

