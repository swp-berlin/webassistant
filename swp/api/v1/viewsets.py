from django.db.models import ProtectedError

from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet

from swp.api.authentication import SessionAuthentication, TokenAuthentication

from .exceptions import ProtectedErrorException
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

        return ModelViewSet.handle_exception(self, exc)
