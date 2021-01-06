from __future__ import annotations

from asgiref.sync import async_to_sync, sync_to_async
from django.db import models, transaction
from django.db.models.aggregates import Count
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from swp.utils.scraping import Scraper as _Scraper

from .abstract import ActivatableModel, ActivatableQuerySet
from .choices import Interval, ScraperType
from .publication import Publication
from .fields import ChoiceField


class ScraperQuerySet(ActivatableQuerySet):

    def annotate_error_count(self, to_attr='') -> ScraperQuerySet:
        return self.annotate(**{to_attr or 'error_count': Count('errors')})


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

    type = ChoiceField(_('type'), choices=ScraperType.choices)

    data = models.JSONField(_('data'))

    start_url = models.URLField(_('start URL'))
    checksum = models.CharField(_('checksum'), max_length=64, unique=True, blank=True, null=True)

    interval = models.PositiveIntegerField(_('interval'), choices=Interval.choices, default=Interval.DAILY)
    last_run = models.DateTimeField(_('last run'), blank=True, null=True)
    created = models.DateTimeField(_('created'), default=timezone.now, editable=False)

    objects = ScraperQuerySet.as_manager()

    class Meta(ActivatableModel.Meta):
        get_latest_by = 'last_run'
        indexes = [models.Index(fields=['-last_run'])]
        verbose_name = _('scraper')
        verbose_name_plural = _('scrapers')

    def __str__(self) -> str:
        return f'[{self.checksum}] {self.thinktank.name}'

    @cached_property
    def error_count(self) -> int:
        return self.errors.count()

    def scrape(self):
        scraper = _Scraper(self.start_url)

        self.async_scrape(scraper, self.data, self.thinktank)

    @async_to_sync
    async def async_scrape(self, scraper, config, thinktank):
        async for data in scraper.scrape(config):
            authors = [data.pop('author', '')]

            publication = Publication(
                **data,
                thinktank=thinktank,
                last_access=timezone.now(),
                ris_type='UNPB' if 'pdf_url' in data else 'ICOMM',
                authors=authors,
            )

            await self.save_publication(publication)

    @sync_to_async
    def save_publication(self, publication):
        if not self.scraped_publications.filter(url=publication.url).exists():
            publication.save()
            self.scraped_publications.add(publication)

    @transaction.atomic
    def save_publications(self, publications):
        Publication.objects.bulk_create(publications)
        self.scraped_publications.add(*publications)
