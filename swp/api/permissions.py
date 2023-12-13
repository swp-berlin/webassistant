from typing import Union

from rest_framework.permissions import SAFE_METHODS, BasePermission

from swp.models import Thinktank, Monitor


class BaseSafeViewPermission(BasePermission):

    def is_safe(self, request, view):
        raise NotImplementedError


class CanManagePool(BaseSafeViewPermission):

    def is_safe(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj: Union[Thinktank, Monitor]):
        return self.is_safe(request, view) or request.user.can_manage_pool(obj.pool)
