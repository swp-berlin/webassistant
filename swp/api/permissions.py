from typing import Union

from rest_framework.permissions import SAFE_METHODS, BasePermission, DjangoModelPermissions

from swp.models import Thinktank, Monitor, ActivatableModel


class BaseSafeViewPermission(BasePermission):

    def is_safe(self, request, view):
        raise NotImplementedError


class HasDjangoModelPermission(DjangoModelPermissions):
    perms_map = {
        **DjangoModelPermissions.perms_map,
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
    }


class HasActivatablePermission(HasDjangoModelPermission):

    def has_object_permission(self, request, view, obj: ActivatableModel):
        if view.action == 'activate':
            if obj.is_active:
                return obj.can_deactivate(request.user)
            else:
                return obj.can_activate(request.user)

        return super().has_object_permission(request, view, obj)


class CanManagePool(BaseSafeViewPermission):

    def is_safe(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj: Union[Thinktank, Monitor]):
        return self.is_safe(request, view) or request.user.can_manage_pool(obj.pool)
