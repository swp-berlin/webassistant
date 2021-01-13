from django.db.models import Prefetch
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from cosmogo.utils.settings import truthy

from swp.api.v1.router import router
from swp.api.v1.serializers import ScraperListSerializer, ThinktankSerializer, ThinktankListSerializer
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

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=truthy(is_active))

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return ThinktankListSerializer

        return super().get_serializer_class()

    @action(detail=True)
    def scrapers(self, request, pk=None):
        # XXX Nested route exists for development purposes only
        queryset = Scraper.objects.annotate_error_count().filter(
            thinktank_id=pk
        )

        serializer = ScraperListSerializer(queryset, many=True)
        return Response(serializer.data)
