from contextlib import contextmanager
from pathlib import Path
from typing import NamedTuple, List

from django.conf import settings
from django.utils import translation
from django.utils.translation import gettext_lazy


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


def trans(string):
    """
    This is just an alias for gettext lazy with the difference that
    words tagged with it won't be found by gettext but are still
    translated by existing translation files containing the word.
    This is useful to use standard translations from django for
    words that we copied from django.
    """

    return gettext_lazy(string)


class GetTextCommandMixin:
    APPLICATION: str
    LOCALE_DIR = Path('locale')

    @property
    def language_codes(self) -> List[str]:
        return [code for code, name in settings.LANGUAGES]

    @classmethod
    def get_filepath(cls, language, domain) -> str:
        """
        Returns the path for a pofile with the supplied
        domain in the specified language.
        """

        return str(cls.LOCALE_DIR / language / 'LC_MESSAGES' / f'{domain}.po')

    @staticmethod
    def key(entry) -> tuple:
        return entry.msgid, entry.msgid_plural
