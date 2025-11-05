from rest_framework.decorators import action
from rest_framework.response import Response

from swp.api.v1.viewsets import ActivatableViewSet
from swp.models import Scraper
from swp.tasks import preview_scraper

from .exceptions import ScraperActiveException
from .filters import ScraperFilterSet
from .serializers import ScraperSerializer, ScraperPreviewSerializer


@ActivatableViewSet.register('scraper')
class ScraperViewSet(ActivatableViewSet):
    serializer_class = ScraperSerializer
    filterset_class = ScraperFilterSet
    queryset = Scraper.objects

    def check_object_permissions(self, request, obj: Scraper):
        super().check_object_permissions(request, obj)

        if self.action in {'update', 'partial_update'} and obj.is_active:
            raise ScraperActiveException

    @action(['POST'], detail=True, serializer_class=ScraperPreviewSerializer)
    def preview(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @action(detail=False, url_path=r'preview/(?P<task_id>[a-z0-9-]+)', serializer_class=ScraperPreviewSerializer)
    def preview_status(self, request, *, task_id: str, **kwargs):
        result = preview_scraper.AsyncResult(task_id)
        serializer = self.get_serializer(instance=result)

        return Response(serializer.data)
