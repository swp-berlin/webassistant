from rest_framework.viewsets import ReadOnlyModelViewSet

from swp.api import default_router
from swp.api.serializers import PoolSerializer
from swp.models import Pool


@default_router.register('pool', basename='pool')
class PoolViewSet(ReadOnlyModelViewSet):
    serializer_class = PoolSerializer
    queryset = Pool.objects
