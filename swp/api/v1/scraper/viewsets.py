from django.db import models
from django.db.models import Prefetch

from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response

from swp.api.v1.viewsets import ActivatableViewSet
from swp.models import Category, Scraper
from swp.tasks import preview_scraper, run_scraper

from .exceptions import ScraperActiveException
from .filters import ScraperFilterSet
from .serializers import (
    ScraperSerializer,
    ScraperPreviewSerializer,
    ScraperRunSerializer,
)


@ActivatableViewSet.register('scraper')
class ScraperViewSet(ActivatableViewSet):
    serializer_class = ScraperSerializer
    filterset_class = ScraperFilterSet
    queryset = Scraper.objects.alias(
        name=models.F('thinktank__name'),
    ).prefetch_related(
        Prefetch('categories', Category.objects.only('id')),
    )

    def check_object_permissions(self, request, obj: Scraper):
        super().check_object_permissions(request, obj)

        if self.action in {'update', 'partial_update'} and obj.is_active:
            raise ScraperActiveException

    @extend_schema(operation_id='scraper_preview_start')
    @action(['PATCH'], detail=True, serializer_class=ScraperPreviewSerializer)
    def preview(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(operation_id='scraper_preview_status')
    @action(detail=False, url_path=r'preview/(?P<task_id>[a-z0-9-]+)', serializer_class=ScraperPreviewSerializer)
    def preview_status(self, request, **kwargs):
        return self.base_status(request, preview_scraper, **kwargs)

    @extend_schema(operation_id='scraper_run')
    @action(['POST'], detail=True, serializer_class=ScraperRunSerializer)
    def run(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(operation_id='scraper_run_status')
    @action(detail=False, url_path=r'run/(?P<task_id>[a-z0-9-]+)', serializer_class=ScraperRunSerializer)
    def run_status(self, request, **kwargs):
        return self.base_status(request, run_scraper, **kwargs)

    def base_status(self, request, task, *, task_id: str, **kwargs):
        result = task.AsyncResult(task_id)
        serializer = self.get_serializer(instance=result)

        return Response(serializer.data)
