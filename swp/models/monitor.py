from __future__ import annotations

import datetime
import operator

from collections import defaultdict
from functools import reduce
from typing import Iterable, Tuple, Collection

from django.db import models
from django.db.models.expressions import Case, ExpressionWrapper, F, When
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

from elasticsearch.exceptions import ElasticsearchException
from elasticsearch_dsl.query import QueryString

from sentry_sdk import capture_message, capture_exception

from swp.db.expressions import MakeInterval
from swp.utils.ris import generate_ris_data
from swp.utils.translation import get_language
from swp.utils.validation import get_field_validation_error

from .pool import CanManageQuerySet
from .publication import Publication
from .fields import ZoteroKeyField, ZOTERO_URI_PATTERN
from .abstract import ActivatableModel, ActivatableQuerySet
from .choices import Interval
from .publicationcount import PublicationCount
from .zotero import ZoteroTransfer


class MonitorQuerySet(ActivatableQuerySet, CanManageQuerySet):
    pool_ref = models.OuterRef('pool')

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
        return self.annotate_next_run(now=now).filter(next_run__lt=end)

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


class Monitor(PublicationCount, ActivatableModel):
    """
    Monitoring profile for a topic of interest.
    """

    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    pool = models.ForeignKey('swp.Pool', models.PROTECT, verbose_name=_('pool'), related_name='monitors')
    query = models.TextField(_('query'), blank=True)
    recipients = ArrayField(models.EmailField(), blank=True, verbose_name=_('recipients'))
    zotero_keys = ArrayField(
        ZoteroKeyField(),
        blank=True,
        default=list,
        verbose_name=_('Zotero keys'),
        help_text='{API_KEY}/(users|groups)/{USER_OR_GROUP_ID}/[collections/{COLLECTION_ID}/]items',
    )

    interval = models.PositiveIntegerField(_('interval'), choices=Interval.choices, default=Interval.DAILY)
    last_sent = models.DateTimeField(_('last sent'), blank=True, null=True)
    created = models.DateTimeField(_('created'), default=timezone.now, editable=False)

    objects = MonitorManager()

    class Meta(ActivatableModel.Meta):
        verbose_name = _('monitor')
        verbose_name_plural = _('monitors')
        constraints = [
            models.CheckConstraint(
                check=models.Q(is_active=False) | ~models.Q(query=''),
                name='active_monitor_has_query',
            ),
        ]

    def __str__(self) -> str:
        return self.name

    def clean(self):
        if self.is_active and not self.query:
            raise get_field_validation_error('query', _('An active monitor must not have an empty query.'))

    def get_publication_ids(self, language=None, using=None):
        from swp.documents import PublicationDocument

        language = get_language(language)
        fields = PublicationDocument.get_search_fields(language)
        search = PublicationDocument.search(using=using).query(
            QueryString(query=self.query, fields=fields, default_operator='AND')
        )

        search.source(False)

        try:
            return [result.meta.id for result in search.scan()]
        except ElasticsearchException as error:
            capture_exception(error)

        return None

    def get_query(self, language=None, using=None):
        if ids := self.get_publication_ids(language, using):
            return models.Q(id__in=ids)

        return models.Q(id=None)

    @property
    def as_query(self):
        return self.get_query(None)

    @property
    def recipient_count(self):
        return len(self.recipients)

    def get_publications(self, *, exclude_sent: bool = False):
        qs = Publication.objects.filter(self.as_query)

        if exclude_sent and self.last_sent:
            qs = qs.filter(last_access__gte=self.last_sent)

        return qs

    @property
    def publications(self):
        return self.get_publications()

    @property
    def new_publications(self) -> Iterable[Publication]:
        return self.get_publications(exclude_sent=True)

    def update_publication_count(self, commit: bool = True, now=None) -> Tuple[int, int]:
        return self.get_publication_counts(self.last_sent, commit=commit, now=timezone.localtime(now))

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

    def get_zotero_publication_keys(self, fail_silently: bool = False) -> Collection[Tuple[str, str, Iterable[str]]]:
        api_key_path_combinations = set()
        collections = defaultdict(set)

        for key in self.zotero_keys:
            try:
                api_key, path, collection_id = self.get_zotero_info(key)
            except ValueError as err:
                if fail_silently:
                    continue

                raise err

            api_key_path_combinations.add((api_key, path))

            if collection_id:
                collections[(api_key, path)].add(collection_id)

        return [(api_key, path, list(collections[(api_key, path)])) for api_key, path in api_key_path_combinations]

    @staticmethod
    def get_zotero_info(zotero_key: str) -> Tuple[str, str, str]:
        match = ZOTERO_URI_PATTERN.match(zotero_key)

        if not match:
            message = f'Invalid Zotero key: {zotero_key}'
            capture_message(message, level='error')
            raise ValueError(message)

        user_or_group_path = match.group('path')
        path = f'{user_or_group_path}/items'

        return match.group('api_key'), path, match.group('collection_id')

    @property
    def transferred_count(self) -> int:
        return self.get_transferred_count(None)

    def get_transferred_count(self, language=None, using=None) -> int:
        zotero_infos = self.get_zotero_publication_keys()

        if not zotero_infos:
            return 0

        publication_ids = self.get_publication_ids(language, using)

        if not publication_ids:
            return 0

        query = reduce(operator.or_, [
            models.Q(api_key=api_key, path=path, collection_keys__contains=collections)
            for api_key, path, collections in zotero_infos
        ])

        queryset = ZoteroTransfer.objects.filter(
            query,
            last_transferred__gte=F('updated'),
            publication__in=publication_ids,
        ).values(
            'publication',  # group by
        ).alias(
            count=models.Count('*'),
        ).filter(
            count=len(zotero_infos),
        )

        return queryset.count()
