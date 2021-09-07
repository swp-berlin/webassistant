from __future__ import annotations

import datetime
import operator
from collections import defaultdict
from functools import reduce
from typing import Iterable, Tuple

from django.db import models
from django.db.models.expressions import Case, ExpressionWrapper, F, When
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

from sentry_sdk import capture_message

from swp.db.expressions import MakeInterval
from swp.utils.ris import generate_ris_data
from .publication import Publication
from .fields import ZoteroKeyField
from .abstract import ActivatableModel, ActivatableQuerySet
from .choices import Interval


class MonitorQuerySet(ActivatableQuerySet):

    def annotate_next_run(self, to_attr: str = '', *, now: datetime.datetime = None) -> MonitorQuerySet:
        next_run = Case(
            When(last_sent=None, then=timezone.localtime(now)),
            default=ExpressionWrapper(
                F('last_sent') + MakeInterval(hours=F('interval')),
                output_field=models.DateTimeField(default=None),
            )
        )

        return self.annotate(**{to_attr or 'next_run': next_run})

    def next_run_before(self, end: datetime.datetime, *, now: datetime.datetime = None) -> MonitorQuerySet:
        scheduled = models.Q(next_run__lt=end)
        return self.annotate_next_run(now=now).complex_filter(scheduled)

    def next_run_between(
        self,
        start: datetime.datetime,
        end: datetime.datetime, *,
        now: datetime.datetime = None,
    ) -> MonitorQuerySet:
        assert end >= start, 'Scheduling time frame mix-up'
        scheduled = models.Q(next_run__gte=start, next_run__lt=end)
        return self.annotate_next_run(now=now).filter(scheduled)

    def scheduled_during_next_hour(self, now: datetime.datetime = None) -> MonitorQuerySet:
        """ Filter monitors scheduled to be sent during the next hour. """
        now = timezone.localtime(now)
        start = now.replace(minute=0, second=0, microsecond=0)
        end = start + datetime.timedelta(hours=1)

        return self.active().next_run_before(end, now=now)


class MonitorManager(models.Manager.from_queryset(MonitorQuerySet, 'BaseMonitorManager')):
    use_in_migrations = True


class Monitor(ActivatableModel):
    """
    Monitoring profile for a topic of interest.
    """

    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    recipients = ArrayField(models.EmailField(), blank=True, verbose_name=_('recipients'))
    zotero_keys = ArrayField(
        ZoteroKeyField(),
        blank=True,
        default=list,
        verbose_name=_('Zotero keys'),
        help_text='{API_KEY}/(users|groups)/{USER_OR_GROUP_ID}/(items|collections|...)',
    )

    interval = models.PositiveIntegerField(_('interval'), choices=Interval.choices, default=Interval.DAILY)
    last_sent = models.DateTimeField(_('last sent'), blank=True, null=True)
    created = models.DateTimeField(_('created'), default=timezone.now, editable=False)

    publication_count = models.PositiveIntegerField(_('publication count'), default=0, editable=False)
    new_publication_count = models.PositiveIntegerField(_('new publication count'), default=0, editable=False)

    objects = MonitorManager()

    class Meta(ActivatableModel.Meta):
        verbose_name = _('monitor')
        verbose_name_plural = _('monitors')

    def __str__(self) -> str:
        return self.name

    @property
    def as_query(self):
        thinktank_filters = self.thinktank_filters.all()
        queries = [thinktank_filter.as_query for thinktank_filter in thinktank_filters]

        return reduce(operator.or_, queries, models.Q())

    @property
    def recipient_count(self):
        return len(self.recipients)

    def get_publications(self, exclude_sent=False):
        qs = Publication.objects.active().filter(self.as_query)

        if exclude_sent and self.last_sent:
            qs = qs.filter(last_access__gte=self.last_sent)

        return qs

    @property
    def publications(self):
        return self.get_publications()

    @property
    def new_publications(self) -> Iterable[Publication]:
        return self.get_publications(exclude_sent=True)

    def update_publication_count(self, commit: bool = True) -> Tuple[int, int]:
        publications = Publication.objects.active().filter(self.as_query)

        self.publication_count = publications.count()

        if self.last_sent:
            self.new_publication_count = publications.filter(last_access__gte=self.last_sent).count()
        else:
            self.new_publication_count = self.publication_count

        for filter in self.thinktank_filters.all():
            filter.update_publication_count(last_sent=self.last_sent)

        if commit:
            self.save(update_fields=['publication_count', 'new_publication_count'])

        return self.publication_count, self.new_publication_count

    @cached_property
    def next_run(self) -> datetime.datetime:
        """ Next scheduled email dispatch to all recipients. """
        next_run = timezone.localtime(self.last_sent)
        if self.last_sent:
            next_run += datetime.timedelta(hours=self.interval)

        return next_run

    def generate_ris_data(self, exclude_sent: bool = False) -> bytes:
        publications = self.get_publications(exclude_sent=exclude_sent)
        return generate_ris_data(publications)

    @property
    def is_zotero(self) -> bool:
        return bool(self.zotero_keys)

    def get_zotero_publication_keys(self, fail_silently: bool = False) -> Iterable[Tuple[str, str, Iterable[str]]]:
        collections = defaultdict(set)
        paths = {}

        for key in self.zotero_keys:
            api_key, sep, path = key.partition('/')
            path = f'{sep}{path}'

            if '/collections/' in path:
                parts = path.split('/')
                if parts[3] != 'collections':
                    capture_message(f'Invalid Zotero collection key: {key}', level='error')
                    if fail_silently:
                        continue

                prefix = '/'.join(parts[:3])
                collection_id = parts[4]
                collections[api_key].add(collection_id)

                # We only post to items so adjust the API here to reflect that
                path = f'{prefix}/items'

            paths[api_key] = path

        return [
            (api_key, path, list(collections[api_key])) for api_key, path in paths.items()
        ]
