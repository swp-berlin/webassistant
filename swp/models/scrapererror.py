from __future__ import annotations

from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.text import Truncator
from django.utils.translation import gettext_lazy as _

from .choices import ErrorLevel
from .fields import ChoiceField


DEFAULT_ERROR = ''  # FIXME


class ScraperErrorQuerySet(models.QuerySet):

    def error_only(self) -> ScraperErrorQuerySet:
        return self.filter(level=ErrorLevel.ERROR)


class ScraperError(models.Model):
    """
    Error encountered during scraping.
    """

    scraper = models.ForeignKey(
        'swp.Scraper',
        on_delete=models.CASCADE,
        related_name='errors',
        verbose_name=_('scraper'),
    )

    publication = models.ForeignKey(
        'swp.Publication',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='errors',
        verbose_name=_('publication'),
    )

    identifier = models.CharField(_('identifier'), max_length=255, blank=True)
    field = models.CharField(_('field'), max_length=50, blank=True)

    level = ChoiceField(
        _('level'),
        choices=ErrorLevel.choices,
        default=ErrorLevel.ERROR,
    )

    code = models.CharField(_('error code'), max_length=8, default=DEFAULT_ERROR)
    message = models.TextField(_('message'))
    timestamp = models.DateTimeField(_('timestamp'), default=timezone.now, editable=False)

    objects = ScraperErrorQuerySet.as_manager()

    class Meta:
        get_latest_by = 'timestamp'
        verbose_name = _('scraping error')
        verbose_name_plural = _('scraping errors')

    def __str__(self) -> str:
        return self.identifier or self.message

    @cached_property
    def source(self) -> str:
        if self.publication_id:
            return self.publication.title or self.publication.url

        return self.identifier

    @classmethod
    def normalize_identifier(cls, value: str) -> str:
        value = str.strip(value or '')
        max_length = cls._meta.get_field('identifier').max_length

        return Truncator(value).chars(max_length)

    @property
    def is_error(self) -> bool:
        return self.level == ErrorLevel.ERROR

    @property
    def is_warning(self) -> bool:
        return self.level == ErrorLevel.WARNING
