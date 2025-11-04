from django.db.models import Prefetch

from swp.api.v1.viewsets import SWPViewSet
from swp.models import Category, Publication, Scraper

from .filters import PublicationFilterSet
from .serializers import PublicationSerializer


@SWPViewSet.register('publication')
class PublicationViewSet(SWPViewSet):
    serializer_class = PublicationSerializer
    filterset_class = PublicationFilterSet
    queryset = Publication.objects.prefetch_related(
        Prefetch('scrapers', Scraper.objects.only('id')),
        Prefetch('categories', Category.objects.only('id')),
    )
