from swp.api.v1.viewsets import SWPViewSet
from swp.models import Monitor

from .filters import MonitorFilterSet
from .serializers import MonitorSerializer


@SWPViewSet.register('monitor')
class MonitorViewSet(SWPViewSet):
    serializer_class = MonitorSerializer
    filterset_class = MonitorFilterSet
    queryset = Monitor.objects
    ordering_fields = SWPViewSet.ordering_fields + [
        'last_sent',
    ]
