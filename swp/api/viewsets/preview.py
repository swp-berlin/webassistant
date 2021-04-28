from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from swp.api import default_router
from swp.api.serializers.preview import PreviewSerializer
from swp.tasks.scraper import preview_scraper


@default_router.register('preview', basename='preview')
class PreviewScraperViewSet(ViewSet):
    serializer_class = PreviewSerializer

    def retrieve(self, request, *, pk):
        result = preview_scraper.AsyncResult(pk)

        serializer = PreviewSerializer(instance=result)

        return Response(serializer.data)

    def create(self, request):
        serializer = PreviewSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
