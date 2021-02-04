from rest_framework import viewsets

from swp.api.v1 import router
from swp.api.v1.serializers.monitor import MonitorSerializer
from swp.models import Monitor


@router.register('monitor', basename='monitor')
class MonitorViewSet(viewsets.ModelViewSet):
    queryset = Monitor.objects.prefetch_related('thinktank_filters__publication_filters')
    serializer_class = MonitorSerializer
