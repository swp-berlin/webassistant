from django_filters.rest_framework import FilterSet
from rest_framework import viewsets

from swp.api.v1 import router
from swp.api.v1.filters import UpdatePublicationCountFilter
from swp.api.v1.serializers.thinktankfilter import ThinktankFilterSerializer
from swp.models import ThinktankFilter


class ThinktankFilterFilterSet(FilterSet):
    update_publications = UpdatePublicationCountFilter()

    class Meta:
        model = ThinktankFilter
        fields = ['update_publications']


@router.register('thinktankfilter', basename='thinktankfilter')
class ThinktankFilterViewSet(viewsets.ModelViewSet):
    queryset = ThinktankFilter.objects.prefetch_related('publication_filters')
    serializer_class = ThinktankFilterSerializer
    filterset_class = ThinktankFilterFilterSet
