from swp.api.v1.viewsets import SWPViewSet
from swp.models import Thinktank

from .filters import ThinktankFilterSet
from .serializers import ThinktankSerializer


@SWPViewSet.register('thinktank')
class ThinktankViewSet(SWPViewSet):
    serializer_class = ThinktankSerializer
    filterset_class = ThinktankFilterSet
    queryset = Thinktank.objects
