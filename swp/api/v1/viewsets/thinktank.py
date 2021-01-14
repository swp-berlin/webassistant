from django.db.models import Prefetch
from rest_framework import viewsets

from swp.api.v1.router import router
from swp.api.v1.serializers import ThinktankSerializer, ThinktankListSerializer
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

        return super().get_serializer_class()

