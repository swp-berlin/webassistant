from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from swp.api.v1.router import router
from swp.api.v1.serializers import ScraperSerializer, ThinktankSerializer, ThinktankListSerializer
from swp.models import Scraper, Thinktank


@router.register('thinktank', basename='thinktank')
class ThinktankViewSet(viewsets.ModelViewSet):
    queryset = Thinktank.objects.annotate_last_run().annotate_counts()
    filterset_fields = ['is_active']
    serializer_class = ThinktankSerializer
    list_serializer_class = ThinktankListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'retrieve':
            queryset = queryset.prefetch_related(
                Prefetch(
                    'scrapers', Scraper.objects.annotate_error_count(),
                ),
            )

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return ThinktankListSerializer
        elif self.action == 'add_scraper':
            return ScraperSerializer

        return super().get_serializer_class()

    def related_scraper_action(self, request, thinktank=None, status=200):
        thinktank = thinktank or self.get_object()
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(thinktank=thinktank)

        return Response(serializer.data, status=status)

    @action(detail=True, methods=['post'], url_name='add-scraper', url_path='add-scraper')
    def add_scraper(self, request, **kwargs):
        return self.related_scraper_action(request)
