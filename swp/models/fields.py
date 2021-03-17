from django.core.exceptions import ImproperlyConfigured
from django.db.models import CharField, URLField

from .constants import MAX_URL_LENGTH


class ChoiceField(CharField):

    def __init__(self, verbose_name=None, *, choices, **kwargs):
        max_length = max(map(len, dict(choices)))
        (default, label), *others = choices

        kwargs.setdefault('max_length', max_length)
        kwargs.setdefault('default', default)
        kwargs.setdefault('db_index', True)

        super(ChoiceField, self).__init__(verbose_name=verbose_name, choices=choices, **kwargs)


class LongURLField(URLField):

    def __init__(self, verbose_name: str = None, *, max_length: int = None, **kwargs):
        max_length = max_length or MAX_URL_LENGTH
        if max_length < MAX_URL_LENGTH:
            raise ImproperlyConfigured('Long URL field must have a length of at least %d' % MAX_URL_LENGTH)

        super().__init__(verbose_name, max_length=max_length, **kwargs)
