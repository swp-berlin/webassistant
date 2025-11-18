from swp.api.v1.viewsets import SWPViewSet
from swp.models import Pool

from .serializers import PoolSerializer


@SWPViewSet.register('pool')
class PoolViewSet(SWPViewSet):
    serializer_class = PoolSerializer
    queryset = Pool.objects
