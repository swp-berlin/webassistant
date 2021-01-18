from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from swp.api.v1.router import router
from swp.api.v1.serializers import PublicationSerializer
from swp.models import Publication


class PublicationPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'


@router.register('publication', basename='publication')
class PublicationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Publication.objects.all()
    filterset_fields = ['thinktank_id']
    ordering = ['-created']
    pagination_class = PublicationPagination
    serializer_class = PublicationSerializer
