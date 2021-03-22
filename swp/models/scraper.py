from __future__ import annotations

import datetime
import hashlib
import json
from typing import Any, Iterable, Mapping, TYPE_CHECKING

from asgiref.sync import async_to_sync, sync_to_async
from django.db import models, transaction, IntegrityError
from django.db.models.aggregates import Count
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from swp.utils.scraping import Scraper as _Scraper
from swp.scraper.types import ScraperType

from .abstract import ActivatableModel, ActivatableQuerySet, UpdateQuerySet, LastModified
from .choices import Interval
from .fields import ChoiceField
from .publication import Publication
from .scrapererror import ScraperError

if TYPE_CHECKING:
    from .thinktank import Thinktank


def get_hash(fields: Mapping[str, Any]) -> str:
    val = json.dumps(fields, sort_keys=True)
    return hashlib.md5(val.encode('utf-8')).hexdigest()


class ScraperQuerySet(ActivatableQuerySet, UpdateQuerySet):

    def annotate_error_count(self, to_attr='') -> ScraperQuerySet:
        return self.annotate(**{to_attr or 'error_count': Count('errors')})


class Scraper(ActivatableModel, LastModified):
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
    is_running = models.BooleanField(_('is running'), default=False, editable=False)

    objects = ScraperQuerySet.as_manager()

    class Meta(ActivatableModel.Meta):
        get_latest_by = 'last_run'
        indexes = [models.Index(fields=['-last_run'])]
        verbose_name = _('scraper')
        verbose_name_plural = _('scrapers')

    def __str__(self) -> str:
        return f'[{self.checksum}] {self.thinktank.name}'

    @cached_property
    def name(self) -> str:
        return _('%s Scraper') % self.thinktank.name

    @cached_property
    def next_run(self):
        last_run = timezone.localtime(self.last_run)

        if self.last_run:
            last_run += datetime.timedelta(hours=self.interval)

        return last_run

    @cached_property
    def error_count(self) -> int:
        return self.errors.count()

    @cached_property
    def unique_fields(self):
        return self.thinktank.unique_fields

    def scrape(self):
        scraper = _Scraper(self.start_url)

        self.async_scrape(scraper, self.data, self.thinktank)

    @async_to_sync
    async def async_scrape(
        self,
        scraper: _Scraper,
        config: Mapping[str, Any],
        thinktank: Thinktank,
    ):
        results = scraper.scrape(config)

        try:
            async for result in results:
                fields = result.get('fields')
                errors = result.get('errors')
                now = timezone.now()

                is_complete = await self.check_scraped_fields(fields, errors, now=now)
                if not is_complete:
                    continue

                publication = Publication(
                    thinktank=thinktank,
                    ris_type='UNPB' if 'pdf_url' in fields else 'ICOMM',
                    last_access=now,
                    created=now,
                    **fields
                )

                try:
                    await self.save_publication(publication)
                except IntegrityError as exc:
                    publication_error = ScraperError(
                        scraper=self,
                        message=str(exc),
                        code='database',  # TODO Define error codes for global classification
                        timestamp=now,
                    )

                    await self.save_error(publication_error)

                if not publication.pk:
                    # the publication is a duplicate, stop scraping
                    scraper.stop()

                if errors:
                    scraper_errors = [
                        ScraperError(
                            scraper=self,
                            message=error.get('message') or _('Scraping Error'),
                            publication_id=publication.pk,
                            field=field,
                            level=error.get('level'),
                            timestamp=now,
                        ) for field, error in errors.items()
                    ]

                    await self.save_errors(scraper_errors)
        finally:
            await results.aclose()

    async def check_scraped_fields(
        self,
        fields: Mapping[str, Any],
        errors: Mapping[str, Any], *,
        now: datetime.datetime,
    ) -> bool:
        """
        Validate scraped publication data for missing fields.

        :return: ``True`` if publication is complete, otherwise ``False``.
        """
        title = fields.get('title')
        url = fields.get('url')

        if title and url:
            return True

        if not title and not url:
            message = _('Missing title and URL')
            field = ''
        elif not title:
            error_message = errors.get('title', {}).get('message', '')
            message = error_message or _('Missing title for %s') % url
            field = 'title'
        elif not url:
            error_message = errors.get('url', {}).get('message', '')
            message = error_message or _('Missing URL element for "%s"') % title

            field = 'url'

        field_error = ScraperError(
            scraper=self,
            identifier=ScraperError.make_identifier(title, url),
            message=message,
            field=field,
            code='missing',
            timestamp=now,
        )

        await self.save_error(field_error)

        return False

    @sync_to_async
    def save_publication(self, publication):
        hash = get_hash({field: getattr(publication, field, '') for field in self.unique_fields})
        if not self.scraped_publications.filter(hash=hash).exists():
            publication.hash = hash
            publication.save()
            self.scraped_publications.add(publication)

    @transaction.atomic
    def save_publications(self, publications):
        Publication.objects.bulk_create(publications)
        self.scraped_publications.add(*publications)

    @sync_to_async
    def save_error(self, error: ScraperError):
        error.save(force_insert=True)

    @sync_to_async
    def save_errors(self, errors: Iterable[ScraperError]):
        ScraperError.objects.bulk_create(errors)
