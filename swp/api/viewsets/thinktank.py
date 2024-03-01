from django.db.models import Prefetch

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from swp.api.permissions import CanManagePool, HasActivatablePermission
from swp.api.router import default_router
from swp.api.serializers import ScraperDraftSerializer, ThinktankSerializer, ThinktankListSerializer
from swp.models import Scraper, Thinktank
from swp.utils.permission import has_perm


class HasThinktankPermission(HasActivatablePermission):

    def has_object_permission(self, request, view, obj: Thinktank):
        if view.action == 'add_scraper':
            return has_perm(request.user, Scraper, 'add')

        return super().has_object_permission(request, view, obj)


@default_router.register('thinktank', basename='thinktank')
class ThinktankViewSet(ModelViewSet):
    permission_classes = [HasThinktankPermission & CanManagePool]
    queryset = Thinktank.objects.annotate_last_run().annotate_counts().prefetch_related('pool').order_by('name')
    filterset_fields = ['pool', 'is_active']
    serializer_class = ThinktankSerializer

    def get_queryset(self):
        queryset = ModelViewSet.get_queryset(self).annotate_can_manage(self.request.user)

        if self.action == 'retrieve':
            queryset = queryset.prefetch_related(
                Prefetch('scrapers', Scraper.objects.annotate_error_count()),
            )

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return ThinktankListSerializer

        return self.serializer_class

    def related_scraper_action(self, request, thinktank=None, status=200):
        thinktank = thinktank or self.get_object()
        serializer = self.get_serializer(data=request.data, thinktank=thinktank)

        serializer.is_valid(raise_exception=True)
        serializer.save(thinktank=thinktank)

        return Response(serializer.data, status=status)

    @action(detail=True, methods=['post'], url_name='add-scraper', url_path='add-scraper',
            serializer_class=ScraperDraftSerializer)
    def add_scraper(self, request, **kwargs):
        return self.related_scraper_action(request)
