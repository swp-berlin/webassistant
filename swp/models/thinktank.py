from __future__ import annotations

import datetime

from typing import Optional

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.aggregates import Count, Max
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from swp.utils.domain import is_subdomain
from swp.utils.validation import get_field_validation_error

from .abstract import ActivatableModel, ActivatableQuerySet
from .choices import UniqueKey
from .fields import ChoiceField, DomainField
from .pool import CanManageQuerySet
from .scraper import Scraper


def get_default_unique_fields():
    return [UniqueKey.URL.value]


class ZeroIfSubqueryNull(Coalesce):

    def __init__(self, queryset):
        Coalesce.__init__(self, models.Subquery(queryset), 0)

    def get_group_by_cols(self, alias=None):
        for exp in self.source_expressions:
            return exp.get_group_by_cols(alias=alias)


class ThinktankQuerySet(ActivatableQuerySet, CanManageQuerySet):
    pool_ref = models.OuterRef('pool')

    def annotate(self, *args, **kwargs) -> ThinktankQuerySet:
        # noinspection PyTypeChecker
        return super().annotate(*args, **kwargs)

    def annotate_counts(self) -> ThinktankQuerySet:
        return (
            self
            .annotate_publication_count()
            .annotate_scraper_count()
            .annotate_active_scraper_count()
            .annotate_last_error_count()
        )

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

    def annotate_last_error_count(self) -> ThinktankQuerySet:
        return self.annotate(
            last_error_count=ZeroIfSubqueryNull(
                Scraper.objects.values(
                    'thinktank',
                ).filter(
                    thinktank=models.OuterRef('id'),
                    last_run__isnull=False,
                ).annotate_error_count().values(
                    'error_count',
                ).order_by(
                    '-last_run',
                )[:1],
            ),
        )

    def for_domain(self, domain: str) -> Optional['Thinktank']:
        return self.filter(domain=domain, is_active=True).first()


class Thinktank(ActivatableModel):
    """
    Source of publications.
    """

    pool = models.ForeignKey('swp.Pool', models.PROTECT, verbose_name=_('pool'), related_name='thinktanks')
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    url = models.URLField(_('URL'), help_text=_('Link to homepage'))
    domain = DomainField(_('domain'), max_length=100)
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
        constraints = [
            models.UniqueConstraint(
                fields=['domain'],
                condition=models.Q(is_active=True),
                name='unique_active_domain',
            ),
        ]

    def __str__(self) -> str:
        return self.name

    def validate_unique(self, exclude=None):
        super().validate_unique(exclude)

        if not self.is_active or (exclude and 'domain' in exclude):
            return None

        self.validate_unique_domain(self.domain, self.id)

    @classmethod
    def validate_unique_domain(cls, domain: str, exclude: int = None):
        if duplicate := cls.objects.exclude(id=exclude).for_domain(domain):
            raise get_field_validation_error(
                field='domain',
                message=_('The domain %(domain)s is already assigned to thinktank %(thinktank)s in pool %(pool)s.'),
                params={'domain': domain, 'thinktank': duplicate, 'pool': duplicate.pool},
                code='unique',
            )

    def deactivate_incompatible_scrapers(self) -> int:
        scrapers = self.scrapers.filter(is_active=True).values_list('id', 'start_url')
        unrelated = [scraper for scraper, url in scrapers if not self.is_subdomain(url)]

        if unrelated:
            return scrapers.filter(id__in=unrelated).update(is_active=False)

        return 0

    def is_subdomain(self, url: str) -> bool:
        return is_subdomain(url, self.domain)

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
        return max([scraper.last_run for scraper in self.scrapers.all() if scraper.last_run is not None], default=None)

    @cached_property
    def last_error_count(self) -> int:
        return getattr(self.last_scraper, 'error_count', 0)
