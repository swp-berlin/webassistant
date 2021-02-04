from django_filters.rest_framework import FilterSet, ModelChoiceFilter
from django.utils.translation import gettext_lazy as _

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from swp.api.v1.router import router
from swp.api.v1.serializers import PublicationSerializer
from swp.models import Monitor, Publication


class PublicationPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class MonitorFilter(ModelChoiceFilter):

    def filter(self, qs, monitor: Monitor):
        query = monitor.as_query
        return qs.filter(query)


class PublicationFilter(FilterSet):
    monitor = MonitorFilter(queryset=Monitor.objects.all(), label=_('Monitor'))

    class Meta:
        model = Publication
        fields = ['thinktank_id', 'monitor']


@router.register('publication', basename='publication')
class PublicationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Publication.objects.all()
    filterset_class = PublicationFilter
    ordering = ['-last_access', '-created']
    pagination_class = PublicationPagination
    serializer_class = PublicationSerializer
