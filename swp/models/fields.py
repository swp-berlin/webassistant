import re

from django.core.exceptions import ImproperlyConfigured
from django.core.validators import RegexValidator
from django.db.models import CharField, URLField
from django.utils.translation import gettext_lazy as _

from swp.utils.isbn import canonical_isbn, normalize_isbn
from .constants import MAX_COMBINED_ISBN_LENGTH, MAX_URL_LENGTH


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


class CombinedISBNField(CharField):
    description = _('Flexible ISBN or ISSN identifier')

    def __init__(self, verbose_name: str = None, *, max_length: int = None, canonical: bool = False, **kwargs):
        max_length = max_length or MAX_COMBINED_ISBN_LENGTH
        super().__init__(verbose_name, max_length=max_length, **kwargs)

        self.canonical = canonical

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if not self.canonical:
            kwargs.pop('canonical', None)

        return name, path, args, kwargs

    def formfield(self, **kwargs):
        defaults = {
            'min_length': 8,
        }

        defaults.update(kwargs)
        return super().formfield(**defaults)

    def clean_value(self, value: str) -> str:
        return (canonical_isbn if self.canonical else normalize_isbn)(value)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)

        cleaned_value = self.clean_value(value)
        setattr(model_instance, self.attname, cleaned_value)

        return super().pre_save(model_instance, add)


# Regex that matches ZOTERO URIs with an API Key prepended
#
# Valid Examples :
#
# P9NiFoyLeZu2bZNvvuQPDWsd/users/1234567/items/
# P9NiFoyLeZu2bZNvvuQPDWsd/users/1234567/collections/ABC123XY/items/
# P9NiFoyLeZu2bZNvvuQPDWsd/groups/1234567/items
# P9NiFoyLeZu2bZNvvuQPDWsd/groups/1234567/collections/ABC123XY/items
ZOTERO_URI_REGEX = (
    r'^'
    r'(?P<api_key>[a-zA-Z0-9]+)'
    r'(?P<path>'
    r'/((users/(?P<user_id>\d+))|(groups/(?P<group_id>\d+)))'
    r')'
    r'(/collections/(?P<collection_id>[23456789ABCDEFGHIJKLMNPQRSTUVWXYZ]{8}))?'
    r'/items/?'
    r'$'
)

ZOTERO_URI_PATTERN = re.compile(ZOTERO_URI_REGEX)


class ZoteroKeyValidator(RegexValidator):
    regex = ZOTERO_URI_REGEX


class ZoteroKeyField(CharField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 255)
        super().__init__(*args, **kwargs)

        self.validators.append(ZoteroKeyValidator())


class ZoteroObjectKeyValidator(RegexValidator):
    # see https://www.zotero.org/support/dev/web_api/v3/write_requests#object_keys
    regex = r'[23456789ABCDEFGHIJKLMNPQRSTUVWXYZ]{8}'


class ZoteroObjectKeyField(CharField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 8)
        super().__init__(*args, **kwargs)
        self.validators.append(ZoteroObjectKeyValidator())
