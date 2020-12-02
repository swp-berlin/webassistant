from asgiref.sync import sync_to_async
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from swp.utils.scraping import Scraper as _Scraper

from .abstract import ActivatableModel
from .choices import Interval
from .publication import Publication


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
    checksum = models.CharField(_('checksum'), max_length=64, unique=True, blank=True, null=True)

    interval = models.PositiveIntegerField(_('interval'), choices=Interval.choices, default=Interval.DAILY)
    last_run = models.DateTimeField(_('last run'), blank=True, null=True)
    created = models.DateTimeField(_('created'), default=timezone.now, editable=False)

    class Meta:
        verbose_name = _('scraper')
        verbose_name_plural = _('scrapers')

    def __str__(self) -> str:
        return f'[{self.checksum}] {self.thinktank.name}'

    async def scrape(self):
        scraper = _Scraper(self.start_url)
        result = await scraper.scrape(self.data)

        last_access = timezone.now()

        publications = []

        for data in result:
            authors = [data.pop('author', '')]

            publications.append(
                Publication(
                    **data,
                    thinktank=self.thinktank,
                    last_access=last_access,
                    ris_type='UNPB' if 'pdf_url' in data else 'ICOMM',
                    authors=authors,
                )
            )

        await self.save_publications(publications)

    @sync_to_async
    @transaction.atomic
    def save_publications(self, publications):
        Publication.objects.bulk_create(publications)
        self.scraped_publications.add(*publications)
