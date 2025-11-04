from swp.api.v1.viewsets import SWPViewSet
from swp.models import PublicationList

from .serializers import PublicationListSerializer


@SWPViewSet.register('publication-list', basename='publication-list')
class PublicationListViewSet(SWPViewSet):
    serializer_class = PublicationListSerializer
    queryset = PublicationList.objects.prefetch_related('entries')

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
