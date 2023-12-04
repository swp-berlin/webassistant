from __future__ import annotations

import datetime
from typing import Optional

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.aggregates import Count, Max
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from .abstract import ActivatableModel, ActivatableQuerySet
from .choices import UniqueKey
from .fields import ChoiceField
from .scraper import Scraper


def get_default_unique_fields():
    return [UniqueKey.URL.value]


class ThinktankQuerySet(ActivatableQuerySet):

    def annotate_counts(self) -> ThinktankQuerySet:
        return self.annotate_publication_count().annotate_scraper_count().annotate_active_scraper_count()

    def annotate_publication_count(self, to_attr='') -> ThinktankQuerySet:
        return self.annotate(**{to_attr or 'publication_count': Count('publications', distinct=True)})

    def annotate_scraper_count(self, to_attr='') -> ThinktankQuerySet:
        return self.annotate(**{to_attr or 'scraper_count': Count('scrapers', distinct=True)})

    def annotate_active_scraper_count(self, to_attr='') -> ThinktankQuerySet:
        count = Count('scrapers', models.Q(scrapers__is_active=True), distinct=True)
        return self.annotate(**{to_attr or 'active_scraper_count': count})

    def annotate_error_count(self, to_attr='') -> ThinktankQuerySet:
        return self.annotate(**{to_attr or 'error_count': Count('scrapers__errors')})

    def annotate_last_run(self, to_attr='') -> ThinktankQuerySet:
        return self.annotate(**{to_attr or 'last_run': Max('scrapers__last_run')})


class Thinktank(ActivatableModel):
    """
    Source of publications.
    """

    pool = models.ForeignKey('swp.Pool', models.PROTECT, verbose_name=_('pool'), related_name='thinktanks')
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    url = models.URLField(_('URL'), help_text=_('Link to homepage'))
    unique_fields = ArrayField(
        verbose_name=_('unique fields'),
        base_field=ChoiceField(choices=UniqueKey.choices),
        default=get_default_unique_fields,
    )
    created = models.DateTimeField(_('created'), default=timezone.now, editable=False)

    objects = ThinktankQuerySet.as_manager()

    class Meta(ActivatableModel.Meta):
        verbose_name = _('think tank')
        verbose_name_plural = _('think tanks')

    def __str__(self) -> str:
        return self.name

    @cached_property
    def publication_count(self) -> int:
        return self.publications.count()

    @cached_property
    def scraper_count(self) -> int:
        return self.scrapers.count()

    @cached_property
    def active_scraper_count(self) -> int:
        return self.scrapers.active().count()

    @cached_property
    def error_count(self) -> int:
        return sum(scraper.errors.count() for scraper in self.scrapers.all())

    def get_last_scraper(self) -> Optional[Scraper]:
        return self.scrapers.filter(last_run__isnull=False).annotate_error_count().order_by('-last_run').first()

    last_scraper = cached_property(get_last_scraper)

    @cached_property
    def last_run(self) -> Optional[datetime.datetime]:
        runs = [scraper.last_run for scraper in self.scrapers.all() if scraper.last_run is not None]
        return max(runs) if runs else None

    @cached_property
    def last_error_count(self) -> int:
        return getattr(self.last_scraper, 'error_count', 0)
