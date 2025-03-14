import re

from django.contrib.postgres.fields import ArrayField, CICharField
from django.core.exceptions import ImproperlyConfigured
from django.core.validators import RegexValidator
from django.db.models import CharField, FloatField, URLField
from django.utils.translation import gettext_lazy as _

from swp.utils.isbn import canonical_isbn, normalize_isbn
from swp.validators import validate_canonical_domain

from .constants import MAX_COMBINED_ISBN_LENGTH, MAX_URL_LENGTH


class CharArrayField(ArrayField):

    def __init__(self, *, max_length: int, **kwargs):
        blank = kwargs.setdefault('blank', False)

        super().__init__(CharField(max_length=max_length, blank=blank), **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = ArrayField.deconstruct(self)

        if base_field := kwargs.pop('base_field', None):
            kwargs.setdefault('max_length', base_field.max_length)

        return name, path, args, kwargs


class ChoiceField(CharField):

    def __init__(self, verbose_name=None, *, choices, **kwargs):
        max_length = max(map(len, dict(choices)))
        (default, label), *others = choices

        kwargs.setdefault('max_length', max_length)
        kwargs.setdefault('default', default)
        kwargs.setdefault('db_index', True)

        super(ChoiceField, self).__init__(verbose_name=verbose_name, choices=choices, **kwargs)


class DomainField(CICharField):
    default_validators = [validate_canonical_domain]


class LongURLField(URLField):

    def __init__(self, verbose_name: str = None, *, max_length: int = None, **kwargs):
        max_length = max_length or MAX_URL_LENGTH
        if max_length < MAX_URL_LENGTH:
            raise ImproperlyConfigured(f'Long URL field must have a length of at least {MAX_URL_LENGTH}.')

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


class DenseVectorField(ArrayField):

    def __init__(self, verbose_name: str = None, *, dims: int, **kwargs):
        kwargs['verbose_name'] = verbose_name
        kwargs['base_field'] = FloatField()
        kwargs['size'] = dims

        ArrayField.__init__(self, **kwargs)

    @property
    def dims(self):
        return self.size

    def deconstruct(self):
        name, path, args, kwargs = ArrayField.deconstruct(self)

        kwargs['dims'] = kwargs.pop('size')

        kwargs.pop('base_field', None)

        return name, path, args, kwargs


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
    default_validators = [ZoteroObjectKeyValidator()]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 8)
        super().__init__(*args, **kwargs)
