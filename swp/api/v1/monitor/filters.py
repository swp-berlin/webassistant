from swp.api.v1.filters import SWPFilterSet
from swp.models import Monitor


class MonitorFilterSet(SWPFilterSet):

    class Meta:
        model = Monitor
        fields = [
            'name',
            'pool',
            'is_active',
        ]
