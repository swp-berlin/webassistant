import django_filters as filters

from django.db import models
from django.utils.translation import gettext_lazy as _

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from swp.api.router import default_router
from swp.api.serializers import PublicationSerializer
from swp.documents import PublicationDocument
from swp.models import Monitor, Publication, ThinktankFilter
from swp.utils.translation import get_language


class PublicationPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class MonitorFilter(filters.ModelChoiceFilter):

    def filter(self, qs, monitor: Monitor):
        if monitor:
            return qs.filter(monitor.as_query)

        return qs


class ThinktankFilterFilter(filters.ModelChoiceFilter):

    def filter(self, qs, thinktankfilter: ThinktankFilter):
        if thinktankfilter:
            return qs.filter(thinktankfilter.as_query)

        return qs


class PublicationFilter(filters.FilterSet):
    monitor = MonitorFilter(label=_('Monitor'), queryset=Monitor.objects)
    thinktankfilter = ThinktankFilterFilter(label=_('Think Tank Filter'), queryset=ThinktankFilter.objects)
    since = filters.DateTimeFilter('last_access', 'gte')
    is_active = filters.BooleanFilter('thinktank__is_active')
    query = filters.CharFilter(method='filter_by_query')

    class Meta:
        model = Publication
        fields = [
            'thinktank_id',
            'monitor',
            'thinktankfilter',
            'since',
        ]

    def filter_by_query(self, queryset, name, value, *, using=None):
        assert name == 'query'

        language = get_language(request=self.request)
        fields = PublicationDocument.get_search_fields(language)
        search = PublicationDocument.search(
            using=using,
        ).query(
            'simple_query_string',
            query=value,
            fields=fields,
        ).extra(
            size=PublicationPagination.page_size * 5,
        ).source(
            excludes=['*'],  # only ids
        )

        ids = [result.meta.id for result in search]

        return queryset.filter(
            id__in=ids,
        ).annotate(
            ordering=models.Case(
                *[models.When(id=pk, then=order) for order, pk in enumerate(ids)],
                output_field=models.PositiveIntegerField(default=0),
            ),
        ).order_by(
            'ordering',
        )


@default_router.register('publication', basename='publication')
class PublicationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Publication.objects
    filterset_class = PublicationFilter
    ordering = ['-last_access', '-created']
    pagination_class = PublicationPagination
    serializer_class = PublicationSerializer
