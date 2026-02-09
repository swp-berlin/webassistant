from swp.api.v1.viewsets import ActivatableViewSet
from swp.models import Thinktank

from .filters import ThinktankFilterSet
from .serializers import ThinktankSerializer


@ActivatableViewSet.register('thinktank')
class ThinktankViewSet(ActivatableViewSet):
    serializer_class = ThinktankSerializer
    filterset_class = ThinktankFilterSet
    queryset = Thinktank.objects
    ordering_fields = ActivatableViewSet.ordering_fields[:-1]
