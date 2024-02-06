from __future__ import annotations

from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from .choices import ErrorLevel
from .constants import MAX_TITLE_LENGTH
from .fields import ChoiceField, LongURLField


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

    title = models.CharField(_('title'), max_length=MAX_TITLE_LENGTH, blank=True)
    url = LongURLField(_('url'), blank=True)
    field = models.CharField(_('field'), max_length=50, blank=True)

    level = ChoiceField(
        _('level'),
        choices=ErrorLevel.choices,
        default=ErrorLevel.ERROR,
    )

    code = models.CharField(_('error code'), max_length=8, default=DEFAULT_ERROR)
    message = models.TextField(_('message'))
    timestamp = models.DateTimeField(_('timestamp'), default=timezone.now, editable=False)
    sent = models.DateTimeField(_('sent'), null=True, editable=False)

    objects = ScraperErrorQuerySet.as_manager()

    class Meta:
        get_latest_by = 'timestamp'
        verbose_name = _('scraping error')
        verbose_name_plural = _('scraping errors')

    def __str__(self) -> str:
        return self.source or self.message

    @cached_property
    def scraped_title(self) -> str:
        return self.publication.title if self.publication_id else self.title

    @cached_property
    def scraped_url(self) -> str:
        return self.publication.url if self.publication_id else self.url

    @cached_property
    def source(self) -> str:
        return (self.publication.title or self.publication.url) if self.publication_id else (self.title or self.url)

    @property
    def is_error(self) -> bool:
        return self.level == ErrorLevel.ERROR

    @property
    def is_warning(self) -> bool:
        return self.level == ErrorLevel.WARNING
