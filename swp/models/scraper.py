from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .abstract import ActivatableModel


class Scraper(ActivatableModel):
    """
    Extractor of publication data.
    """

    thinktank = models.ForeignKey(
        'swp.Thinktank',
        on_delete=models.CASCADE,
        related_name='scrapers',
        verbose_name=_('think tank'),
    )

    type = models.ForeignKey(
        'swp.ScraperType',
        on_delete=models.CASCADE,
        related_name='scrapers',
        verbose_name=_('type'),
    )

    data = models.JSONField(_('data'))

    start_url = models.URLField(_('start URL'))
    checksum = models.CharField(_('checksum'), max_length=64, unique=True)

    interval = models.IntegerField(_('interval'))
    last_run = models.DateTimeField(_('last run'), blank=True, null=True)
    created = models.DateTimeField(_('created'), default=timezone.now, editable=False)

    class Meta:
        verbose_name = _('scraper')
        verbose_name_plural = _('scrapers')

    def __str__(self) -> str:
        return f'[{self.checksum}] {self.thinktank.name}'
