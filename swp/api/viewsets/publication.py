import operator

from contextlib import suppress
from functools import reduce, lru_cache
from typing import List

import django_filters as filters

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from django_elasticsearch_dsl.search import Search
from elasticsearch import BadRequestError
from elasticsearch_dsl.aggs import Terms
from elasticsearch_dsl.query import Match, QueryString, Range, Knn

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission, IsAuthenticated

from swp.api.exceptions import InvalidQueryError, FullTextSearchError
from swp.api.router import default_router
from swp.api.serializers import PublicationSerializer, ResearchSerializer, BucketSerializer
from swp.documents import PublicationDocument
from swp.models import Monitor, Pool, Publication, User
from swp.utils.embedding import embed_query
from swp.utils.ris import RISResponse
from swp.utils.translation import get_language

BUCKETS = [
    'tags',
    'categories',
]


class CanResearch(BasePermission):

    def has_permission(self, request, view):
        return request.user.can_research


class PublicationPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class ResearchPagination(PublicationPagination):

    def __init__(self):
        self.buckets = {}

    def paginate_queryset(self, queryset, request, view=None):
        page = super(ResearchPagination, self).paginate_queryset(queryset, request, view=view)
        response = queryset.execute(ignore_cache=False)

        for bucket in BUCKETS:
            self.buckets[bucket] = response.aggregations[bucket].buckets

        return page

    def get_paginated_response(self, data):
        response = super(ResearchPagination, self).get_paginated_response(data)

        for bucket, values in self.buckets.items():
            response.data[bucket] = BucketSerializer(values, many=True).data

        return response


class MonitorFilter(filters.ModelChoiceFilter):

    def filter(self, qs, monitor: Monitor):
        if monitor:
            return qs.filter(monitor.as_query)

        return qs


class PublicationFilter(filters.FilterSet):
    monitor = MonitorFilter(label=_('Monitor'), queryset=Monitor.objects)
    since = filters.DateTimeFilter('last_access', 'gte')
    is_active = filters.BooleanFilter('thinktank__is_active')

    class Meta:
        model = Publication
        fields = [
            'thinktank_id',
            'monitor',
            'since',
        ]


def get_pool_queryset(request):
    return Pool.objects.can_research(request.user)


@lru_cache(maxsize=50)
def get_query_vector(query: str):
    success, result = embed_query(query)

    if success:
        return result

    elif success is None:
        raise FullTextSearchError from result

    else:
        raise InvalidQueryError


class ResearchFilter(filters.FilterSet):
    start_date = filters.DateFilter(label=_('Start Date'), required=False)
    end_date = filters.DateFilter(label=_('End Date'), required=False)
    query = filters.CharFilter(label=_('Query'), required=True)
    pool = filters.ModelMultipleChoiceFilter(label=_('Pool'), queryset=get_pool_queryset, required=False)

    def filter_queryset(self, queryset, *, using=None):
        data = self.form.cleaned_data
        query = self.get_search_query(**data)
        search = PublicationDocument.search(using=using).query(query)

        for bucket in BUCKETS:
            search.aggs.bucket(bucket, Terms(field=bucket))

        search = search.source(False)

        # Fill response cache, so we avoid an extra count query when paginating.
        search.execute(ignore_cache=True)

        return search

    @staticmethod
    def get_result_queryset(search):
        return Publication.objects.filter(
            id__in=[result.meta.id for result in search],
        ).annotate(
            score=models.Case(
                *[models.When(id=result.meta.id, then=result.meta.score) for result in search],
                output_field=models.FloatField(default=0.),
            ),
        ).order_by(
            '-score',
        )

    def get_search_query(self, query: str, pool=None, start_date=None, end_date=None, *, k=50):
        query, knn = self.parse_query(query)
        language = get_language(request=self.request)
        fields = PublicationDocument.get_search_fields(language)
        query = QueryString(query=query, fields=fields, default_operator='AND')

        if start_date or end_date:
            created = {'time_zone': settings.TIME_ZONE}

            if start_date:
                created['gte'] = start_date

            if end_date:
                created['lte'] = end_date

            query &= Range(created=created)

        if pool_query := self.get_pool_query(pool):
            query &= pool_query

        if knn is None:
            return query

        return Knn(field='embedding', k=k, query_vector=get_query_vector(knn), filter=query)

    @staticmethod
    def parse_query(query: str):
        query, knn = query.strip(), None

        with suppress(ValueError):
            start, end = query.index('<'), query.index('>')

            if start == 0:
                knn = query[1: end].strip() or None
                query = query[end + 1:].strip() or '*'

        return query, knn

    def get_pool_query(self, pool: List[Pool] = None):
        if ids := self.get_pool_ids(self.request.user, pool):
            return reduce(operator.or_, [Match(thinktank__pool=pool) for pool in ids])

    @staticmethod
    def get_pool_ids(user: User, pools: List[Pool] = None):
        if pools:
            return [pool.id for pool in pools]
        elif user.can_research_all_pools:
            return None
        else:
            return user.pools.values_list('id', flat=True)


@default_router.register('publication', basename='publication')
class PublicationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Publication.objects.select_related('thinktank')
    filterset_class = PublicationFilter
    ordering = ['-last_access', '-created']
    pagination_class = PublicationPagination
    serializer_class = PublicationSerializer

    @action(
        detail=False,
        ordering=None,
        filterset_class=ResearchFilter,
        pagination_class=ResearchPagination,
        serializer_class=ResearchSerializer,
        permission_classes=[IsAuthenticated & CanResearch],
    )
    def research(self, request):
        try:
            return self.list(request)
        except BadRequestError as err:
            if err.error == 'search_phase_execution_exception':
                raise InvalidQueryError from err
            raise err

    @action(detail=False, permission_classes=[IsAuthenticated & CanResearch])
    def ris(self, request):
        filterset = ResearchFilter(data=request.GET, queryset=Publication.objects, request=request)

        search: Search = filterset.qs
        search = search.params(preserve_order=True)
        search = search.scan()

        queryset = ResearchFilter.get_result_queryset(search)

        return RISResponse(queryset, filename='export.ris')

    def get_serializer(self, *args, **kwargs):
        if self.action == 'research':
            args = ResearchFilter.get_result_queryset(*args),

        return super(PublicationViewSet, self).get_serializer(*args, **kwargs)
