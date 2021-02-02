from enum import Enum


class ErrorLevel(Enum):
    WARNING = 'Warning'
    ERROR = 'Error'


class ScraperError(Exception):
    pass


class ResolverError(ScraperError):
    def __init__(self, message, level: ErrorLevel = None, **kwargs):
        super().__init__(message)
        self.level = level
