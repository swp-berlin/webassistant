from swp.api.v1.viewsets import SWPViewSet
from swp.models import Scraper

from .filters import ScraperFilterSet
from .serializers import ScraperSerializer


@SWPViewSet.register('scraper')
class ScraperViewSet(SWPViewSet):
    serializer_class = ScraperSerializer
    filterset_class = ScraperFilterSet
    queryset = Scraper.objects
