from celery.canvas import group

from django.db.models import Prefetch

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from swp.api import default_router
from swp.api.permissions import CanManagePool, HasActivatablePermission
from swp.api.serializers import MonitorSerializer, MonitorDetailSerializer, MonitorEditSerializer
from swp.models import Monitor, Pool
from swp.tasks import send_publications_to_zotero, update_publication_count
from swp.utils.permission import has_perm


class HasMonitorPermission(HasActivatablePermission):

    def has_object_permission(self, request, view, obj: Monitor):
        if view.action == 'edit':
            return has_perm(request.user, obj, 'change')

        return super().has_object_permission(request, view, obj)


class CanManageMonitor(CanManagePool):

    def is_safe(self, request, view):
        return CanManagePool.is_safe(self, request, view) and not (view == 'edit')


@default_router.register('monitor', basename='monitor')
class MonitorViewSet(ModelViewSet):
    permission_classes = [HasMonitorPermission & CanManagePool]
    serializer_class = MonitorSerializer
    queryset = Monitor.objects.order_by('name')
    filterset_fields = ['pool']

    def get_queryset(self):
        return ModelViewSet.get_queryset(self).prefetch_related(
            Prefetch('pool', Pool.objects.can_manage(self.request.user)),
        )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MonitorDetailSerializer

        if self.action in {'create', 'update', 'partial_update'}:
            return MonitorEditSerializer

        return self.serializer_class

    def get_serializer(self, instance=None, *, many=None, **kwargs):
        if self.action == 'list':
            group(update_publication_count.s(pk=obj.pk) for obj in instance).delay(model=Monitor._meta.label)
        elif self.action == 'retrieve':
            update_publication_count.delay(Monitor._meta.label, instance.pk)
        elif self.action == 'update_publication_count':
            instance.update_publication_count(now=self.request.now)

        return super(MonitorViewSet, self).get_serializer(instance, many=many, **kwargs)

    @action(detail=True, serializer_class=MonitorEditSerializer)
    def edit(self, request, **kwargs):
        return self.retrieve(request, **kwargs)

    @action(detail=True, methods=['post'], url_path='update-publication-count')
    def update_publication_count(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @action(detail=True, methods=['post'], url_path='transfer-to-zotero')
    def transfer_to_zotero(self, request, **kwargs):
        monitor = self.get_object()

        if not monitor.is_active:
            return Response({'success': False, 'message': 'Monitor needs to be active to sync to Zotero'}, status=400)

        send_publications_to_zotero.delay(monitor.pk)

        return Response({'success': True}, status=200)
