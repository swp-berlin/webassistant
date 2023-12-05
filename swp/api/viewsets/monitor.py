from celery.canvas import group
from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from swp.api import default_router
from swp.api.serializers import MonitorSerializer, MonitorDetailSerializer, ThinktankFilterSerializer
from swp.models import Monitor, ThinktankFilter
from swp.tasks import send_publications_to_zotero, update_publication_count


@default_router.register('monitor', basename='monitor')
class MonitorViewSet(viewsets.ModelViewSet):
    serializer_class = MonitorSerializer
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

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MonitorDetailSerializer
        if self.action == 'add_filter':
            return ThinktankFilterSerializer

        return super().get_serializer_class()

    def related_filter_action(self, request, monitor=None, status=200):
        monitor = monitor or self.get_object()
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(monitor=monitor)

        return Response(serializer.data, status=status)

    def get_serializer(self, instance=None, *, many=None, **kwargs):
        if self.action == 'list':
            group(update_publication_count.s(pk=obj.pk) for obj in instance).delay(model=Monitor._meta.label)
        elif self.action == 'retrieve':
            update_publication_count.delay(Monitor._meta.label, instance.pk)
        elif self.action == 'update_publication_count':
            instance.update_publication_count(now=self.request.now)

        return super(MonitorViewSet, self).get_serializer(instance, many=many, **kwargs)

    @action(detail=True, methods=['post'], url_name='update-publication-count', url_path='update-publication-count')
    def update_publication_count(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @action(detail=True, methods=['post'], url_name='add-filter', url_path='add-filter')
    def add_filter(self, request, **kwargs):
        return self.related_filter_action(request)

    @action(detail=True, methods=['post'], url_name='transfer-to-zotero', url_path='transfer-to-zotero')
    def transfer_to_zotero(self, request, **kwargs):
        monitor = self.get_object()

        if not monitor.is_active:
            return Response({'success': False, 'message': 'Monitor needs to be active to sync to Zotero'}, status=400)

        send_publications_to_zotero.delay(monitor.pk)

        return Response({'success': True}, status=200)
