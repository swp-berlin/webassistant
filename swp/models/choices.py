from django.db import models
from django.utils.translation import gettext_lazy as _

from swp.scraper.types import ListType


class Interval(models.IntegerChoices):
    """
    Frequency of access in hours.
    """
    TWICE_DAILY = 12, _('twice daily')
    DAILY = 24, _('daily')
    WEEKLY = 24 * 7, _('weekly')
    MONTHLY = 24 * 7 * 30, _('monthly')


class ScraperType(models.TextChoices):
    LIST_WITH_DOCS = 'list_with_docs', ListType.name
