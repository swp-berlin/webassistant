from rest_framework.permissions import DjangoModelPermissions, SAFE_METHODS


class SWPModelPermissions(DjangoModelPermissions):
    perms_map = {
        **DjangoModelPermissions.perms_map,
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
    }

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or view.can_manage_pool(request.user, obj)


class ActivatePermission(SWPModelPermissions):
    perms_map = {
        'POST': ['%(app_label)s.activate_%(model_name)s']
    }


class DeactivatePermission(SWPModelPermissions):
    perms_map = {
        'POST': ['%(app_label)s.deactivate_%(model_name)s']
    }
