from enum import Enum
from django.utils.translation import gettext_lazy as _


class ErrorLevel(Enum):
    WARNING = 'warning'
    ERROR = 'error'


class ScraperError(Exception):

    def __init__(self, message: str, *, field: str = '', **kwargs):
        super().__init__(message, **kwargs)
        self.field = field


class ResolverError(ScraperError):
    def __init__(self, message, level: ErrorLevel = None, status: str = '', **kwargs):
        msg = '%s\nStatus: %s' % (message, status)
        super().__init__(msg, **kwargs)
        self.level = level



class CloudflareError(ScraperError):
    def __init__(self, message: str = '', status: str = '', **kwargs):
        message = message or _('Scraping protection prevents page access')
        msg = '%s\nStatus: %s' % (message, status)
        super().__init__(msg, **kwargs)
