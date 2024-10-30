from celery.schedules import crontab
from dotenv import load_dotenv

from pathlib import Path

from swp.utils.settings import env, get_git_commit, password_validators, redis, elasticsearch
from swp.utils.translation import trans

from django.urls import reverse_lazy

BASE_DIR = Path(__file__).parents[2]

load_dotenv(BASE_DIR / '.env')

ENVIRONMENT = env('ENVIRONMENT', 'default')

RELEASE = get_git_commit(BASE_DIR)

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG', False)

SITE_ID = env('SITE_ID', 1)

BASE_URL = 'http://localhost:8000'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': env('DATABASE_HOST', '127.0.0.1'),
        'NAME': env('DATABASE_NAME', 'swp'),
        'USER': env('DATABASE_USER', 'swp'),
        'PASSWORD': env('DATABASE_PASSWORD', 'swp'),
    },
}

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    # Main
    'swp',

    # Extensions
    'django_elasticsearch_dsl',
    'django_filters',
    'rest_framework',

    # Admin
    'swp.apps.AdminConfig',

    # Contrib
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'swp.middleware.now',
]

ROOT_URLCONF = 'swp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'swp.context_processors.settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'swp.wsgi.application'

########
# AUTH #
########

AUTH_USER_MODEL = 'swp.User'

AUTH_PASSWORD_VALIDATORS = password_validators(
    'UserAttributeSimilarityValidator',
    'MinimumLengthValidator',
    'CommonPasswordValidator',
    'NumericPasswordValidator',
)

LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = reverse_lazy('index')
LOGOUT_URL = reverse_lazy('logout')

USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'de'
LANGUAGES = [
    ('de', trans('German')),
    ('en', trans('English')),
]

USE_TZ = True
TIME_ZONE = 'Europe/Berlin'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_STORAGE = 'swp.storage.webpack.WebPackStorage'

MEDIA_ROOT = BASE_DIR / 'media'

WEBPACK_ASSETS_MAP_PATH = BASE_DIR / 'swp' / 'assets' / 'assets.map.json'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '%(levelname)-8s %(asctime)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'detailed-console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'detailed',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['detailed-console'],
            'level': 'INFO',  # set to DEBUG for db queries
        },
        'elk': {
            'handlers': ['detailed-console'],
            'level': 'DEBUG',
        },
        'swp': {
            'handlers': ['detailed-console'],
            'level': 'DEBUG',
        },
    },
}

CELERY_BROKER_URL = CELERY_RESULT_BACKEND = redis(db=SITE_ID)

CELERY_SCRAPER_MONITORING_FILEPATH = BASE_DIR / 'celery-scraper.check'

CELERY_BEAT_SCHEDULE = {
    'monitoring.default': {
        'task': 'monitoring',
        'schedule': crontab(minute='*'),
    },
    'monitoring.scraper': {
        'task': 'monitoring',
        'schedule': crontab(minute='*/15'),
        'options': {
            'queue': 'scraper',
        },
        'kwargs': {
            'filepath': f'{CELERY_SCRAPER_MONITORING_FILEPATH}',
        },
    },
    'monitor.schedule': {
        'task': 'monitor.schedule',
        'schedule': crontab(hour='*', minute=0),
    },
    'monitor.zotero': {
        'task': 'monitor.zotero',
        'schedule': 60 * 60 * 2,  # every 2 hours
    },
    'scraper.schedule': {
        'task': 'scraper.schedule',
        'schedule': crontab(hour='*', minute=0),
    },
    'error-report.send': {
        'task': 'error-report.send',
        'schedule': crontab(hour=7, minute=30),
    },
}

CELERY_TASK_CREATE_MISSING_QUEUES = True

CELERY_TASK_ROUTES = {
    'scraper.run': {
        'queue': 'scraper',
    },
}

ELASTICSEARCH_DSL = {
    'default': elasticsearch(debug=DEBUG),
}

DEBUG_TOOLBAR = False
PLAYWRIGHT_DEBUG = env('PLAYWRIGHT_DEBUG', False)

SHELL_PLUS_PRINT_SQL = env('SHELL_PLUS_PRINT_SQL', False)
SHELL_PLUS_POST_IMPORTS = [
    ('swp.forms', '*'),
    ('swp.models.choices', '*'),
    ('swp.tasks', '*'),
    ('swp.tasks.monitor', '*'),
    ('swp.utils.auth', '*'),
    ('swp.utils.isbn', '*'),
    ('swp.utils.ris', '*'),
    ('swp.utils.zotero', '*'),
]

# <editor-fold desc="REST API">

REST_FRAMEWORK_DEFAULT_RENDERER_CLASSES = [
    'rest_framework.renderers.JSONRenderer',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'swp.api.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': REST_FRAMEWORK_DEFAULT_RENDERER_CLASSES,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
    ],
    'EXCEPTION_HANDLER': 'swp.api.exceptions.exception_handler',
}

# </editor-fold>

# <editor-fold desc="Zotero">

ZOTERO_API_BASE_URL = 'https://api.zotero.org'
ZOTERO_API_VERSION = 3

#: Maximum items per API request
ZOTERO_API_MAX_ITEMS = 50

#: Timeout in seconds for each API request
ZOTERO_API_TIMEOUT = 30

# </editor-fold>

MAIL_PREVIEW_ENABLED = env('MAIL_PREVIEW_ENABLED', DEBUG)

EMBEDDING_SPOOLING_DIR = BASE_DIR / 'spooling'

EMBEDDING_SPOOLING_KEEP_DONE = env('EMBEDDING_SPOOLING_KEEP_DONE', DEBUG)
EMBEDDING_SPOOLING_KEEP_LOST = env('EMBEDDING_SPOOLING_KEEP_LOST', DEBUG)
EMBEDDING_SPOOLING_KEEP_ERROR = env('EMBEDDING_SPOOLING_KEEP_ERROR', True)

EMBEDDING_VECTOR_DIMS = env('EMBEDDING_VECTOR_DIMS', 384)

EMBEDDING_API_HOST = env('EMBEDDING_HOST', 'http://localhost:8080')
