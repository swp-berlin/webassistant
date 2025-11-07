from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action

from swp.api.v1.viewsets import SWPViewSet
from swp.models import PublicationList

from .serializers import (
    PublicationListSerializer,
    PublicationListAddSerializer,
    PublicationListRemoveSerializer,
)


@SWPViewSet.register('publication-list', basename='publication-list')
class PublicationListViewSet(SWPViewSet):
    serializer_class = PublicationListSerializer
    queryset = PublicationList.objects.prefetch_related('entries')

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @extend_schema(operation_id='publication_list_add_publication')
    @action(['POST'], detail=True, serializer_class=PublicationListAddSerializer)
    def add(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(operation_id='publication_list_remove_publication')
    @action(['POST'], detail=True, serializer_class=PublicationListRemoveSerializer)
    def remove(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
