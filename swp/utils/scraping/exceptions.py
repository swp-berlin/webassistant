import os

from enum import Enum
from django.utils.translation import gettext_lazy as _


class ErrorLevel(Enum):
    WARNING = 'warning'
    ERROR = 'error'


class ScraperError(Exception):

    def __init__(self, message: str, *, field: str = ''):
        super().__init__(message)
        self.field = field


class ResponseError(ScraperError):

    def __init__(self, message: str, field: str = '', status: int = 0):
        if status:
            message = f'{message}{os.linesep}Status: {status}'

        super().__init__(message, field=field)
        self.status = status


class ResolverError(ResponseError):

    def __init__(self, message, level: ErrorLevel = None, status: int = 0):
        super().__init__(message, status=status)
        self.level = level


class CloudflareError(ResponseError):

    def __init__(self, message: str = '', status: int = 0):
        super().__init__(message or _('Scraping protection prevents page access.'), status=status)
