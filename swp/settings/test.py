from .base import *

DEBUG = False  # this is the default for tests anyway, just here to make it clear

SECRET_KEY = 'this-is-not-a-secret-key'

TEST_DATA_DIR = BASE_DIR / 'test-data'

TEMPLATES[0]['DIRS'] = [
    # Add our test templates directory.
    TEST_DATA_DIR / 'templates',
]

TEMPLATES[0]['OPTIONS'].update(
    # Always activate template debugging, even in tests,
    # to catch missing templates in include tags.
    debug=True,
)

# speed up logins in tests by using a weak password hasher
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',
]

TEST_RUNNER = 'swp.test.runner.CosmoCodeTestRunner'

MEDIA_ROOT = TEST_DATA_DIR / 'media'

WEBPACK_ASSETS_MAP_PATH = TEST_DATA_DIR / 'assets.map.json'

LOGGING['loggers'] = {
    name: {**config, 'level': 'NOTSET'}
    for name, config in LOGGING.get('loggers').items()
}

SILENCED_SYSTEM_CHECKS = [
    'swp.W001',
]

# We set the redis port to an unassigned port so we
# detect asynchronous task calls that aren't mocked.
CELERY_BROKER_URL = CELERY_RESULT_BACKEND = redis(port=1234)
