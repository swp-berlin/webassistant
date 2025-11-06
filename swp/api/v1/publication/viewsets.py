from django.db.models import Prefetch

from rest_framework.decorators import action
from rest_framework.parsers import JSONParser

from swp.api.v1.viewsets import SWPViewSet
from swp.models import Category, Publication, Scraper

from .filters import PublicationFilterSet
from .pagination import ElasticSearchPagination
from .serializers import PublicationSerializer, PublicationSearchSerializer


@SWPViewSet.register('publication')
class PublicationViewSet(SWPViewSet):
    serializer_class = PublicationSerializer
    filterset_class = PublicationFilterSet
    ordering_fields = [
        'id',
        'title',
        'created',
    ]
    queryset = Publication.objects.prefetch_related(
        Prefetch('scrapers', Scraper.objects.only('id')),
        Prefetch('categories', Category.objects.only('id')),
    )

    @action(
        detail=False,
        methods=['POST'],
        filter_backends=[],
        parser_classes=[JSONParser],
        pagination_class=ElasticSearchPagination,
        serializer_class=PublicationSearchSerializer,
    )
    def search(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
