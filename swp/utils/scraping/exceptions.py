from enum import Enum


class ErrorLevel(Enum):
    WARNING = 'warning'
    ERROR = 'error'


class ScraperError(Exception):

    def __init__(self, message: str, *, field: str = '', **kwargs):
        super().__init__(message, **kwargs)
        self.field = field


class ResolverError(ScraperError):
    def __init__(self, message, level: ErrorLevel = None, **kwargs):
        super().__init__(message, **kwargs)
        self.level = level
