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
