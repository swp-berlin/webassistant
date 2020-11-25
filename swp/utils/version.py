import subprocess

from functools import lru_cache

from django.conf import settings


@lru_cache(maxsize=None)
def get_version():
    try:
        output = subprocess.check_output(['git', 'describe', '--tags'], encoding='utf-8')
    except subprocess.CalledProcessError:
        return settings.RELEASE[:12]

    return str.strip(output)
