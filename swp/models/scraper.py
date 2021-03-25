from __future__ import annotations

import datetime
import hashlib
import json
from typing import Any, Iterable, Mapping, Optional, TYPE_CHECKING

from asgiref.sync import async_to_sync, sync_to_async
from django.core.exceptions import NON_FIELD_ERRORS
from django.db import models, transaction, IntegrityError
from django.db.models.aggregates import Count
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from swp.utils.scraping import Scraper as _Scraper
from swp.scraper.types import ScraperType

from .abstract import ActivatableModel, ActivatableQuerySet, UpdateQuerySet, LastModified
from .choices import ErrorLevel, Interval
from .fields import ChoiceField, LongURLField
from .publication import Publication
from .scrapererror import ScraperError

if TYPE_CHECKING:
    from .thinktank import Thinktank


def get_hash(fields: Mapping[str, Any]) -> str:
    val = json.dumps(fields, sort_keys=True)
    return hashlib.md5(val.encode('utf-8')).hexdigest()


class ScraperQuerySet(ActivatableQuerySet, UpdateQuerySet):

    def annotate_error_count(self, to_attr='') -> ScraperQuerySet:
        error_count = Count('errors', filter=models.Q(errors__level=ErrorLevel.ERROR))
        return self.annotate(**{to_attr or 'error_count': error_count})


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

    start_url = LongURLField(_('start URL'))
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
        return f'{self.name} {self.pk}'

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
        return self.errors.error_only().count()

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

                publication = await self.build_publication(fields, errors, thinktank=thinktank, now=now)
                if publication is None:
                    continue

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

    async def build_publication(
        self,
        fields: Mapping[str, Any],
        errors: Mapping[str, Any], *,
        thinktank: Thinktank,
        now: datetime.datetime,
    ) -> Optional[Publication]:
        # NOTE Must be locally to avoid problems with auth forms importing get_user_model
        from swp.forms import ScrapedPublicationForm

        form = ScrapedPublicationForm(data=fields)
        if form.is_valid():
            return form.save(commit=False, thinktank=thinktank, now=now)

        identifier = ScraperError.normalize_identifier(
            fields.get('title') or fields.get('url'),
        )

        validation_errors = []
        for field, error_list in form.errors.items():
            field_error = errors.get(field, {}).get('message', '')
            for error in error_list.as_data():
                if field_error and error.code in ['required', 'invalid']:
                    message = field_error
                else:
                    message = '\n'.join(error.messages)

                scraper_error = ScraperError(
                    scraper=self,
                    identifier=identifier,
                    message=message,
                    field=field if field != NON_FIELD_ERRORS else '',
                    code=(error.code or 'invalid')[:8],
                    timestamp=now,
                )

                validation_errors.append(scraper_error)

        await self.save_errors(validation_errors)

        return None

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
            identifier=ScraperError.normalize_identifier(title or url),
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
            publication.save(force_insert=True)
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
