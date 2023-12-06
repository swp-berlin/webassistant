from rest_framework.viewsets import ReadOnlyModelViewSet

from swp.api import default_router
from swp.api.serializers import PoolSerializer
from swp.models import Pool


@default_router.register('pool', basename='pool')
class PoolViewSet(ReadOnlyModelViewSet):
    serializer_class = PoolSerializer
    queryset = Pool.objects

    def get_queryset(self):
        return ReadOnlyModelViewSet.get_queryset(self).annotate_can_manage(self.request.user)
