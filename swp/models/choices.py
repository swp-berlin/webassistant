from django.db import models
from django.db.models import enums
from django.utils.translation import gettext_lazy as _


class CodesMeta(enums.ChoicesMeta):

    @property
    def max_length(self) -> int:
        return max(map(len, self.values))


class CodeChoices(models.TextChoices, metaclass=CodesMeta):
    """
    TextChoices with additional model helpers.
    """


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
    STATIC = 'Static', _('Static')

    DOCUMENT = 'Document', _('Document')
    DOI = 'DOI', _('DOI')
    ISBN = 'ISBN', _('ISBN/ISSN')

    TITLE = 'Title', _('Title')
    SUBTITLE = 'Subtitle', _('Subtitle')
    ABSTRACT = 'Abstract', _('Abstract')
    PUBLICATION_DATE = 'Publication_Date', _('Publication Date')
    URL = 'URL', _('URL')
    AUTHORS = 'Authors', _('Authors')
    TAGS = 'Tags', _('Tags')


class ListResolverType(models.TextChoices):
    LINK = ResolverType.LINK

    TITLE = ResolverType.TITLE
    SUBTITLE = ResolverType.SUBTITLE
    ABSTRACT = ResolverType.ABSTRACT
    PUBLICATION_DATE = ResolverType.PUBLICATION_DATE
    URL = ResolverType.URL
    AUTHORS = ResolverType.AUTHORS
    TAGS = ResolverType.TAGS
    DOCUMENT = ResolverType.DOCUMENT
    DOI = ResolverType.DOI
    ISBN = ResolverType.ISBN


class DataResolverKey(models.TextChoices):
    TITLE = 'title', _('Title')
    SUBTITLE = 'subtitle', _('Subtitle')
    ABSTRACT = 'abstract', _('Abstract')
    AUTHORS = 'authors', _('Authors')
    PUBLICATION_DATE = 'publication_date', _('Publication Date')
    URL = 'url', _('URL')
    PDF_URL = 'pdf_url', _('PDF URL')
    DOI = 'doi', _('DOI')
    ISBN = 'isbn', _('ISBN/ISSN')
    TAGS = 'tags', _('Tags')


class UniqueKey(models.TextChoices):
    URL = 'url', _('URL')
    TITLE = 'title', _('Title')


class Comparator(models.TextChoices):
    CONTAINS = 'contains', _('Contains')
    STARTS_WITH = 'starts_with', _('Starts With')
    ENDS_WITH = 'ends_with', _('Ends With')


class PaginatorType(models.TextChoices):
    ENDLESS = 'Endless', _('Endless')
    PAGE = 'Page', _('Page')


class ErrorLevel(CodeChoices):
    WARNING = 'warning', _('Warning')
    ERROR = 'error', _('Error')


class FilterField(models.TextChoices):
    TEXT = 'text', _('Text')

    TITLE = DataResolverKey.TITLE
    SUBTITLE = DataResolverKey.SUBTITLE
    ABSTRACT = DataResolverKey.ABSTRACT
    AUTHORS = DataResolverKey.AUTHORS
    PUBLICATION_DATE = DataResolverKey.PUBLICATION_DATE
    URL = DataResolverKey.URL
    PDF_URL = DataResolverKey.PDF_URL
    DOI = DataResolverKey.DOI
    ISBN = DataResolverKey.ISBN
    TAGS = DataResolverKey.TAGS
