from typing import Iterable, Iterator

from django.utils.translation import gettext_lazy as _


CONJUNCTION_AND = _('%(first)s and %(second)s')
CONJUNCTION_OR = _('%(first)s or %(second)s')
DELIMITER = ', '


def enumeration(words, conjunction=CONJUNCTION_AND, delimiter=DELIMITER):
    if not words:
        return ''

    *first, second = map(str, words)

    if first:
        return conjunction % dict(first=delimiter.join(first), second=second)

    return second


def when(values: Iterable[str]) -> Iterator[str]:
    return filter(None, values)


def spaced(value: str) -> str:
    return ' '.join(when(str.split(value)))
