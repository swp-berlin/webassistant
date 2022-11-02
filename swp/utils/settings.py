import os

from .confirmation import TRUTHY
from .git import get_commit


def env(key, default=None, parser=None):
    value = os.environ.get(key)

    if value is None:
        return default

    if parser is None:
        if default is None:
            parser = str
        else:
            parser = type(default)

    if parser is bool:
        return truthy(value, default)

    return parser(value)


def truthy(value, default=False):
    return TRUTHY.get(value, default)


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


def elasticsearch(*, debug=False, prefix='ELASTICSEARCH'):
    def get(var, default=None):
        return env(f'{prefix}_{var}', default)

    username = get('USERNAME', 'elastic')
    password = get('PASSWORD')
    scheme = get('SCHEME', 'https')
    hostname = get('HOSTNAME', 'localhost')
    port = get('PORT', 9200)
    certs = get('CA_CERTS')
    verify_certs = get('VERIFY_CERTS', not debug)

    if verify_certs is False:
        from urllib3 import disable_warnings
        from urllib3.exceptions import InsecureRequestWarning

        disable_warnings(InsecureRequestWarning)

    return {
        'hosts': f'{scheme}://{username}:{password}@{hostname}:{port}',
        'ca_certs': certs,
        'verify_certs': verify_certs,
    }
