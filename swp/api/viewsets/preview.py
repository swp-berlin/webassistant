from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from swp.api import default_router
from swp.api.permissions import HasDjangoModelPermission
from swp.api.serializers.preview import PreviewSerializer
from swp.models import Scraper
from swp.tasks.scraper import preview_scraper


class CanPreview(HasDjangoModelPermission):

    def _queryset(self, view):
        return Scraper.objects


@default_router.register('preview', basename='preview')
class PreviewScraperViewSet(ViewSet):
    serializer_class = PreviewSerializer
    permission_classes = [CanPreview]

    def retrieve(self, request, *, pk):
        result = preview_scraper.AsyncResult(pk)

        serializer = PreviewSerializer(instance=result)

        return Response(serializer.data)

    def create(self, request):
        serializer = PreviewSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
