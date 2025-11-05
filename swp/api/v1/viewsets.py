from django.db.models import ProtectedError

from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet

from swp.api.authentication import SessionAuthentication, TokenAuthentication
from swp.models import ActivatableModel

from .exceptions import ActiveObjException, ProtectedErrorException
from .filters import SWPFilterSet
from .pagination import SWPagination
from .router import default_router


class SWPViewSet(ModelViewSet):
    pagination_class = SWPagination
    permission_classes = [DjangoModelPermissions]
    authentication_classes = [
        TokenAuthentication,
        SessionAuthentication,
    ]
    filterset_class = SWPFilterSet
    ordering = ['id']
    ordering_fields = [
        'id',
        'name',
        'created',
        'last_modified',
    ]

    @classmethod
    def register(cls, prefix, basename=None):
        return default_router.register(prefix, basename=basename)

    def get_queryset(self):
        return self.queryset.all()

    def handle_exception(self, exc):
        if isinstance(exc, ProtectedError):
            exc = ProtectedErrorException(exc)

        return super().handle_exception(exc)


class ActivatableViewSet(SWPViewSet):

    def get_serializer(self, *args, **kwargs):
        if self.action in {'activate', 'deactivate'}:
            kwargs['activate'] = self.action == 'activate'

        return super().get_serializer(*args, **kwargs)

    @action(['POST'], detail=True)
    def activate(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @action(['POST'], detail=True)
    def deactivate(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def perform_destroy(self, instance: ActivatableModel):
        if instance.is_active:
            raise ActiveObjException(instance)

        return super().perform_destroy(instance)
