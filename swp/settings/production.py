from .base import *

DEBUG = False

ALLOWED_HOSTS = ['production.swp.cosmoco.de', 'production.swp.cosmocode.de']

USE_X_FORWARDED_FOR = True
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')