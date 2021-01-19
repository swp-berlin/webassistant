from django.conf import settings
from django.template.loader import select_template

from .translation import get_language


def get_template(identifier, language=None, fallback=None):
    language = get_language(language=language)
    fallback = fallback or settings.LANGUAGE_CODE

    return select_template([
        f'snippets/{language}/{identifier}.md',
        f'snippets/{fallback}/{identifier}.md',
    ])
