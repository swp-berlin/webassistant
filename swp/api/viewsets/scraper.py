from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from swp.api.permissions import HasActivatablePermission
from swp.api.router import default_router
from swp.api.serializers import ScraperSerializer, ScraperDraftSerializer
from swp.models import Scraper


class HasScraperPermission(HasActivatablePermission):
    pass


class CanManagePool(BasePermission):

    def has_object_permission(self, request, view, obj: Scraper):
        return request.user.can_manage_pool(obj.thinktank.pool)


@default_router.register('scraper', basename='scraper')
class ScraperViewSet(ModelViewSet):
    queryset = Scraper.objects.prefetch_related('thinktank__pool', 'errors')
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
