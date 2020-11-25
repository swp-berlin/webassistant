from contextlib import contextmanager
from typing import NamedTuple


from django.conf import settings
from django.utils import translation


def get_language(language=None, user=None, request=None):
    return (
        language or
        getattr(user, 'language', None) or
        getattr(request, 'LANGUAGE_CODE', None) or
        translation.get_language() or
        settings.LANGUAGE_CODE
    )


@contextmanager
def force_language(language=None, user=None, request=None):
    language = get_language(language, user, request)

    with translation.override(language):
        yield language


class ContentTranslation(NamedTuple):
    type: str
    msgid: str

    def key(self):
        """
        Helper to group a list of content translations by it's type.
        """

        return self.type
