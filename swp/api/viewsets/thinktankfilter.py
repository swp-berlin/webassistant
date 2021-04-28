from django_filters.rest_framework import FilterSet
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from swp.api import default_router
from swp.api.filters import UpdatePublicationCountFilter
from swp.api.serializers import PublicationSerializer
from swp.api.serializers.thinktankfilter import ThinktankFilterSerializer
from swp.models import ThinktankFilter


class ThinktankFilterFilterSet(FilterSet):
    update_publications = UpdatePublicationCountFilter()

    class Meta:
        model = ThinktankFilter
        fields = ['update_publications']


@default_router.register('thinktankfilter', basename='thinktankfilter')
class ThinktankFilterViewSet(viewsets.ModelViewSet):
    queryset = ThinktankFilter.objects.prefetch_related('publication_filters')
    serializer_class = ThinktankFilterSerializer
    filterset_class = ThinktankFilterFilterSet

    def preview_action(self, request, status=200):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        publications = serializer.preview()

        publication_serializer = PublicationSerializer(publications, many=True)

        return Response(publication_serializer.data, status=status)

    @action(detail=False, methods=['post'], url_name='preview', url_path='preview')
    def preview(self, request):
        return self.preview_action(request)
