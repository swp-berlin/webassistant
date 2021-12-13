from django.db.models import Prefetch
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from swp.api import default_router
from swp.api.filters import UpdatePublicationCountFilter
from swp.api.serializers import ThinktankFilterSerializer
from swp.api.serializers.monitor import MonitorSerializer
from swp.models import Monitor, ThinktankFilter
from swp.tasks.monitor import send_publications_to_zotero


class MonitorFilterSet(FilterSet):
    update_publications = UpdatePublicationCountFilter()

    class Meta:
        model = Monitor
        fields = ['update_publications']


@default_router.register('monitor', basename='monitor')
class MonitorViewSet(viewsets.ModelViewSet):
    queryset = Monitor.objects.prefetch_related(
        Prefetch(
            'thinktank_filters',
            queryset=ThinktankFilter.objects.select_related(
                'thinktank',
            ).prefetch_related(
                'publication_filters',
            ).order_by('thinktank__name')
        ),
    ).order_by('name')
    serializer_class = MonitorSerializer
    filterset_class = MonitorFilterSet

    def get_serializer_class(self):
        if self.action == 'add_filter':
            return ThinktankFilterSerializer

        return super().get_serializer_class()

    def related_filter_action(self, request, monitor=None, status=200):
        monitor = monitor or self.get_object()
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(monitor=monitor)

        return Response(serializer.data, status=status)

    @action(detail=True, methods=['post'], url_name='add-filter', url_path='add-filter')
    def add_filter(self, request, **kwargs):
        return self.related_filter_action(request)

    @action(detail=True, methods=['post'], url_name='transfer-to-zotero', url_path='transfer-to-zotero')
    def transfer_to_zotero(self, request, **kwargs):
        monitor = self.get_object()

        send_publications_to_zotero.delay(monitor.pk)

        return Response({'success': True}, status=200)
