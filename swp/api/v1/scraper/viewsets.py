from swp.api.v1.viewsets import ActivatableViewSet
from swp.models import Scraper

from .exceptions import ScraperActiveException
from .filters import ScraperFilterSet
from .serializers import ScraperSerializer


@ActivatableViewSet.register('scraper')
class ScraperViewSet(ActivatableViewSet):
    serializer_class = ScraperSerializer
    filterset_class = ScraperFilterSet
    queryset = Scraper.objects

    def check_object_permissions(self, request, obj: Scraper):
        super().check_object_permissions(request, obj)

        if self.action in {'update', 'partial_update'} and obj.is_active:
            raise ScraperActiveException
