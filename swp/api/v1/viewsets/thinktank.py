from rest_framework import viewsets
from cosmogo.utils.settings import truthy

from swp.api.v1.router import router
from swp.api.v1.serializers import ThinktankSerializer
from swp.models import Thinktank


@router.register('thinktank', basename='thinktank')
class ThinktankViewSet(viewsets.ModelViewSet):
    queryset = Thinktank.objects.annotate_last_run().annotate_counts()
    serializer_class = ThinktankSerializer
    filterset_fields = ['is_active']
