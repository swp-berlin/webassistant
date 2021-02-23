from django.db import models
from django.utils.translation import gettext_lazy as _


class Interval(models.IntegerChoices):
    """
    Frequency of access in hours.
    """
    TWICE_DAILY = 12, _('twice daily')
    DAILY = 24, _('daily')
    WEEKLY = 24 * 7, _('weekly')
    MONTHLY = 24 * 7 * 30, _('monthly')


class ResolverType(models.TextChoices):
    LIST = 'List', _('List')
    LINK = 'Link', _('Link')
    DATA = 'Data', _('Data')
    ATTRIBUTE = 'Attribute', _('Attribute')
    DOCUMENT = 'Document', _('Document')
    STATIC = 'Static', _('Static')
    TAG = 'Tag', _('Tag')
    TAG_DATA = 'TagData', _('Data')
    TAG_ATTRIBUTE = 'TagAttribute', _('Attribute')
    TAG_STATIC = 'TagStatic', _('Static')
    AUTHORS = 'Authors', _('Authors')


class ListResolverType(models.TextChoices):
    LIST = 'List', _('List')
    LINK = 'Link', _('Link')
    FIELD = 'Data', _('Field')
    STATIC = 'Static', _('Static')
    TAG = 'Tag', _('Tag')
    AUTHORS = 'Authors', _('Authors')


class TagResolverType(models.TextChoices):
    TAG_DATA = 'TagData', _('Data')
    TAG_ATTRIBUTE = 'TagAttribute', _('Attribute')
    TAG_STATIC = 'TagStatic', _('Static')


class DataResolverKey(models.TextChoices):
    TITLE = 'title', _('Title')
    SUBTITLE = 'subtitle', _('Subtitle')
    ABSTRACT = 'abstract', _('Abstract')
    AUTHORS = 'authors', _('Authors')
    PUBLICATION_DATE = 'publication_date', _('Publication Date')
    URL = 'url', _('URL')
    PDF_URL = 'pdf_url', _('PDF URL')


class UniqueKey(models.TextChoices):
    URL = 'url', _('URL')
    NAME = 'name', _('Name')


class Comparator(models.TextChoices):
    CONTAINS = 'contains', _('Contains')
    STARTS_WITH = 'starts_with', _('Starts With')
    ENDS_WITH = 'ends_with', _('Ends With')
