import os

from .confirmation import TRUE_FALSE
from .git import get_commit


def env(key, default=None, parser=str):
    value = os.environ.get(key)

    if value is None:
        return default

    return parser(value)


truthy = TRUE_FALSE.get


def debug_toolbar(apps, middleware, active=True, **config):
    """
    Returns configured settings when debug toolbar is available.
    """

    try:
        import debug_toolbar
    except ImportError:
        debug_toolbar = active = False

    ips = ['localhost', '127.0.0.1'] + ['192.168.0.%i' % ip for ip in range(1, 256)]

    if active:
        apps = apps + [debug_toolbar.default_app_config]
        middleware = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + middleware
        config = dict(
            # Hide the debug toolbar by default.
            SHOW_COLLAPSED=True,

            # We disable the rarely used panels
            # by default to improve performance.
            DISABLE_PANELS={
                'debug_toolbar.panels.versions.VersionsPanel',
                'debug_toolbar.panels.timer.TimerPanel',
                'debug_toolbar.panels.settings.SettingsPanel',
                'debug_toolbar.panels.headers.HeadersPanel',
                'debug_toolbar.panels.request.RequestPanel',
                'debug_toolbar.panels.staticfiles.StaticFilesPanel',
                'debug_toolbar.panels.templates.TemplatesPanel',
                'debug_toolbar.panels.cache.CachePanel',
                'debug_toolbar.panels.signals.SignalsPanel',
                'debug_toolbar.panels.logging.LoggingPanel',
                'debug_toolbar.panels.redirects.RedirectsPanel',
            },
        )

    return apps, middleware, ips, active, config


def django_extensions(apps, active=True):
    try:
        import django_extensions
    except ImportError:
        active = False

    if active:
        apps += ['django_extensions']

    return apps


def password_validators(*validators):
    return list(_parse_password_validators(validators))


def _parse_password_validators(validators):
    for validator in validators:
        if isinstance(validator, (tuple, list)):
            validator, options = validator
        else:
            validator, options = validator, {}

        if '.' not in validator:
            validator = 'django.contrib.auth.password_validation.%s' % validator

        yield dict(NAME=validator, OPTIONS=options)


def get_git_commit(path, revision='HEAD'):
    return get_commit(path, revision=revision)


def configure_sentry(dsn, environment, release, celery=False, **kwargs):
    from sentry_sdk import init
    from sentry_sdk.integrations.django import DjangoIntegration

    integrations = [DjangoIntegration()]

    if celery:
        from sentry_sdk.integrations.celery import CeleryIntegration

        integrations.append(CeleryIntegration())

    kwargs['integrations'] = integrations

    return init(dsn=dsn, environment=environment, release=release, **kwargs)


REDIS_DEFAULTS = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
}


def redis(**kwargs):
    defaults = dict(REDIS_DEFAULTS, **kwargs)

    for name in list(defaults):
        default = defaults.get(name)
        parser = type(default)
        variable = str.upper(f'REDIS_{name}')
        defaults[name] = env(variable, default, parser)

    return 'redis://%(host)s:%(port)s/%(db)s' % defaults
