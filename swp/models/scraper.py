from __future__ import annotations

import datetime
import hashlib
import json

from typing import Any, Iterable, Mapping, Optional, TYPE_CHECKING
from urllib.parse import urlsplit

from asgiref.sync import async_to_sync, sync_to_async
from django.core.exceptions import NON_FIELD_ERRORS
from django.db import models, transaction, IntegrityError
from django.db.models.aggregates import Count
from django.shortcuts import resolve_url
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from swp.utils.domain import is_subdomain
from swp.utils.scraping import Scraper as _Scraper
from swp.utils.validation import get_field_validation_error
from swp.scraper.types import ScraperType

from .abstract import ActivatableModel, ActivatableQuerySet, UpdateQuerySet, LastModified
from .choices import ErrorLevel, Interval
from .constants import MAX_TITLE_LENGTH, MAX_URL_LENGTH
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

    def get_absolute_url(self):
        return resolve_url('thinktank:scraper:edit', self.thinktank_id, self.id)

    def clean(self):
        if self.start_url and self.thinktank:
            self.validate_start_url(self.start_url, self.thinktank.domain)

    @staticmethod
    def validate_start_url(start_url: str, domain: str):
        try:
            netloc = urlsplit(start_url).netloc
        except ValueError:
            raise get_field_validation_error('start_url', _('Please enter a valid start url.'))

        if not is_subdomain(netloc, domain):
            raise get_field_validation_error(
                field='start_url',
                message=_("The scraper's start url must be a subdomain of its thinktank's domain (%(domain)s)."),
                params={'domain': domain},
            )

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

    @property
    def full_scan(self) -> bool:
        if not self.last_run:
            return True

        return self.last_modified > self.last_run

    def scrape(self):
        scraper = _Scraper(self.start_url, full_scan=self.full_scan)

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

        #: [SWP-155] Split publication identifier into ``title`` and ``url``
        title = form.truncate(fields.get('title', ''), MAX_TITLE_LENGTH)
        url = fields.get('url', '')[:MAX_URL_LENGTH]

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
                    title=title,
                    url=url,
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

        title = fields.get('title') or ''
        url = fields.get('url') or ''

        if title and url:
            return True

        def get_message(key, fallback, context):
            return key, errors.get(key, {}).get('message', '') or (fallback % context)

        if title:
            field, message = get_message('url', _('Missing URL element for "%s"'), title)
        elif url:
            field, message = get_message('title', _('Missing title for %s'), url)
        else:
            field, message = '', _('Missing title and URL')

        field_error = ScraperError(
            scraper=self,
            title=title[:MAX_TITLE_LENGTH],
            url=url[:MAX_URL_LENGTH],
            message=message,
            field=field,
            code='missing',
            timestamp=now,
        )

        await self.save_error(field_error)

        return False

    @sync_to_async
    def save_publication(self, publication) -> bool:
        publication.hash = get_hash({field: getattr(publication, field, '') for field in self.unique_fields})

        if self.scraped_publications.filter(hash=publication.hash).exists():
            return False

        publication.save(force_insert=True)
        self.scraped_publications.add(publication)

        return True

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
