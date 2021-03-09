from typing import Union

from .exceptions import ErrorLevel, ResolverError


def get_error(error: Union[str, ResolverError], level: ErrorLevel = None):
    level = level or error.level or ErrorLevel.ERROR

    return {'message': str(error), 'level': level.value}
