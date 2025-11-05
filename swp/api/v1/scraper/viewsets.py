from swp.api.v1.viewsets import ActivatableViewSet
from swp.models import Scraper

from .filters import ScraperFilterSet
from .serializers import ScraperSerializer


@ActivatableViewSet.register('scraper')
class ScraperViewSet(ActivatableViewSet):
    serializer_class = ScraperSerializer
    filterset_class = ScraperFilterSet
    queryset = Scraper.objects
