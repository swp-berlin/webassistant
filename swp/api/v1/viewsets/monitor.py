from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from swp.api.v1 import router
from swp.api.v1.serializers import ThinktankFilterSerializer
from swp.api.v1.serializers.monitor import MonitorSerializer
from swp.models import Monitor


@router.register('monitor', basename='monitor')
class MonitorViewSet(viewsets.ModelViewSet):
    queryset = Monitor.objects.prefetch_related('thinktank_filters__publication_filters')
    serializer_class = MonitorSerializer

    def get_serializer_class(self):
        if self.action == 'add_filter':
            return ThinktankFilterSerializer

        return super().get_serializer_class()

    def related_filter_action(self, request, thinktank=None, status=200):
        thinktank = thinktank or self.get_object()
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(thinktank=thinktank)

        return Response(serializer.data, status=status)

    @action(detail=True, methods=['post'], url_name='add-filter', url_path='add-filter')
    def add_filter(self, request, **kwargs):
        return self.related_filter_action(request)
