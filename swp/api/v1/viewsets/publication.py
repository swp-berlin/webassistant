from django_filters.rest_framework import BooleanFilter, FilterSet, ModelChoiceFilter, DateTimeFilter
from django.utils.translation import gettext_lazy as _

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from swp.api.v1.router import router
from swp.api.v1.serializers import PublicationSerializer
from swp.models import Monitor, Publication, ThinktankFilter


class PublicationPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class MonitorFilter(ModelChoiceFilter):

    def filter(self, qs, monitor: Monitor):
        if monitor:
            return qs.filter(monitor.as_query)

        return qs


class ThinktankFilterFilter(ModelChoiceFilter):

    def filter(self, qs, thinktankfilter: ThinktankFilter):
        if thinktankfilter:
            return qs.filter(thinktankfilter.as_query)

        return qs


class PublicationFilter(FilterSet):
    monitor = MonitorFilter(queryset=Monitor.objects.all(), label=_('Monitor'))
    thinktankfilter = ThinktankFilterFilter(queryset=ThinktankFilter.objects.all(), label=_('Think Tank Filter'))
    since = DateTimeFilter('last_access', 'gte')
    is_active = BooleanFilter('thinktank__is_active')

    class Meta:
        model = Publication
        fields = [
            'thinktank_id',
            'monitor',
            'thinktankfilter',
            'since',
        ]


@router.register('publication', basename='publication')
class PublicationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Publication.objects.all()
    filterset_class = PublicationFilter
    ordering = ['-last_access', '-created']
    pagination_class = PublicationPagination
    serializer_class = PublicationSerializer
