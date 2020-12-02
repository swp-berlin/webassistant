from typing import Optional

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField


class Publication(models.Model):
    """
    Single published article.
    """

    thinktank = models.ForeignKey(
        'swp.Thinktank',
        on_delete=models.CASCADE,
        related_name='publications',
        verbose_name=_('think tank'),
    )

    scrapers = models.ManyToManyField(
        'swp.Scraper',
        related_name='scraped_publications',
        verbose_name=_('scrapers'),
    )

    ris_type = models.CharField(_('reference type'), max_length=7, default='ICOMM')  # [TY]
    title = models.CharField(_('title'), max_length=255)  # [T1]
    subtitle = models.CharField(_('subtitle'), max_length=255, blank=True)  # [T2]
    abstract = models.TextField(_('abstract'), blank=True)  # [AB]
    authors = ArrayField(models.CharField(max_length=100), blank=True, null=True, verbose_name=_('authors'))  # [AU]
    publication_date = models.CharField(_('publication date'), max_length=255, blank=True, default='')  # [PY]
    last_access = models.DateTimeField(_('last access'), editable=False, null=True)  # [Y2]
    url = models.URLField(_('URL'))  # [UR]
    pdf_url = models.URLField(_('PDF URL'), blank=True)  # [L1]
    pdf_pages = models.PositiveIntegerField(_('number of pages'), default=0)  # [EP]
    tags = ArrayField(models.CharField(max_length=32), blank=True, null=True, verbose_name=_('tags'))  # [KW]
    created = models.DateTimeField(_('created'), default=timezone.now, editable=False)

    class Meta:
        verbose_name = _('publication')
        verbose_name_plural = _('publications')

    def __str__(self) -> str:
        return self.title

    @property
    def year(self) -> Optional[int]:
        # XXX This might become its own field later, in case the scraped articles do not provide full dates
        return getattr(self.publication_date, 'year', None)
