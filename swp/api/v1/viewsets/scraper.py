from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from swp.models import Scraper

from ..serializers import ScraperSerializer, ScraperDraftSerializer
from ..router import router


@router.register('scraper', basename='scraper')
class ScraperViewSet(ModelViewSet):
    queryset = Scraper.objects.select_related('thinktank').prefetch_related(
        'errors',
    )
    serializer_class = ScraperDraftSerializer

    def get_serializer_class(self):
        if self.action in ['activate', 'retrieve']:
            return ScraperSerializer

        return super().get_serializer_class()

    @action(detail=True, methods=['post'], url_name='activate', url_path='activate')
    def activate(self, request, pk):
        scraper = self.get_object()
        serializer = self.get_serializer(scraper, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
