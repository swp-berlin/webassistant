from celery.schedules import crontab
from dotenv import load_dotenv

from pathlib import Path

from cosmogo.utils.gettext import trans
from cosmogo.utils.settings import env, get_git_commit, password_validators, truthy, redis

from django.urls import reverse_lazy

BASE_DIR = Path(__file__).parents[2]

load_dotenv(BASE_DIR / '.env')

ENVIRONMENT = env('ENVIRONMENT', 'default')

RELEASE = get_git_commit(BASE_DIR)

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG', False, parser=truthy)

SITE_ID = env('SITE_ID', 1, parser=int)

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
    'cosmogo',
    'rest_framework',
    'django_filters',

    # Admin
    'swp.apps.AdminConfig',

    # Contrib
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
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
    'cosmogo.middleware.now',
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
STATICFILES_STORAGE = 'cosmogo.storage.webpack.WebPackStorage'

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

CELERY_BEAT_SCHEDULE = {
    'monitoring': {
        'task': 'monitoring',
        'schedule': crontab(minute='*'),
    },
    'monitor.schedule': {
        'task': 'monitor.schedule',
        'schedule': crontab(hour='*', minute=0),
    },
    'scraper.schedule': {
        'task': 'scraper.schedule',
        'schedule': crontab(hour='*', minute=0),
    },
}

CELERY_TASK_CREATE_MISSING_QUEUES = True

CELERY_TASK_ROUTES = {
    'scraper.run': {
        'queue': 'scraper',
    },
}

DEBUG_TOOLBAR = False

SHELL_PLUS_PRINT_SQL = env('SHELL_PLUS_PRINT_SQL', default=False, parser=truthy)
SHELL_PLUS_POST_IMPORTS = [
    ('swp.forms', '*'),
    ('swp.models.choices', '*'),
    ('swp.tasks', '*'),
    ('swp.utils.ris', '*'),
]

# <editor-fold desc="REST API">

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
    ],
}

# </editor-fold>
