from pathlib import Path

from celery.app import shared_task

from django.conf import settings
from django.core.management import call_command as django_call_command

DEFAULT_CELERY_MONITORING_FILEPATH = Path(settings.BASE_DIR) / 'celery.check'


@shared_task(name='call-command')
def call_command(name, *args, **kwargs):
    return django_call_command(name, *args, **kwargs)


@shared_task(bind=True, name='monitoring')
def monitoring(task, filepath=None):
    filepath = get_monitoring_filepath(task, filepath=filepath)

    with open(filepath, 'w') as fp:
        fp.write(task.request.id)


def get_monitoring_filepath(task, filepath=None, default=DEFAULT_CELERY_MONITORING_FILEPATH):
    if filepath is None:
        filepath = getattr(settings, f'{task.app.namespace}_MONITORING_FILEPATH', default)

    return filepath
