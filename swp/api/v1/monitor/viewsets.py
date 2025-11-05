from swp.api.v1.viewsets import ActivatableViewSet
from swp.models import Monitor

from .filters import MonitorFilterSet
from .serializers import MonitorSerializer


@ActivatableViewSet.register('monitor')
class MonitorViewSet(ActivatableViewSet):
    serializer_class = MonitorSerializer
    filterset_class = MonitorFilterSet
    queryset = Monitor.objects
    ordering_fields = ActivatableViewSet.ordering_fields + [
        'last_sent',
    ]
