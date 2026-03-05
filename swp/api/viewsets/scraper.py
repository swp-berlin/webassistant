from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from swp.api.permissions import HasActivatablePermission
from swp.api.router import default_router
from swp.api.serializers import ScraperSerializer, ScraperDraftSerializer
from swp.models import Scraper
from swp.tasks import run_scraper


class HasScraperPermission(HasActivatablePermission):
    pass


class CanManagePool(BasePermission):

    def has_object_permission(self, request, view, obj: Scraper):
        return request.user.can_manage_pool(obj.thinktank.pool)


@default_router.register('scraper', basename='scraper')
class ScraperViewSet(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Scraper.objects.prefetch_related('thinktank__pool', 'errors', 'categories')
    serializer_class = ScraperDraftSerializer
    permission_classes = [HasScraperPermission & CanManagePool]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ScraperSerializer

        return self.serializer_class

    @action(detail=True, methods=['post'], serializer_class=ScraperSerializer)
    def activate(self, request, pk):
        scraper = self.get_object()
        serializer = self.get_serializer(scraper, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], serializer_class=ScraperSerializer)
    def scrape(self, request, pk):
        try:
            run_scraper.delay(pk, force=True)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'msg': 'Scraper was started'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], serializer_class=ScraperSerializer)
    def is_running(self, request, pk):
        scraper = self.get_object()
        return Response({'isRunning': scraper.is_running}, status=status.HTTP_200_OK)
