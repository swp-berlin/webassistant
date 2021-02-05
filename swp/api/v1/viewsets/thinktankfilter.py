from rest_framework import viewsets

from swp.api.v1 import router
from swp.api.v1.serializers.thinktankfilter import ThinktankFilterSerializer
from swp.models import ThinktankFilter


@router.register('thinktankfilter', basename='thinktankfilter')
class ThinktankFilterViewSet(viewsets.ModelViewSet):
    queryset = ThinktankFilter.objects.prefetch_related('publication_filters')
    serializer_class = ThinktankFilterSerializer
