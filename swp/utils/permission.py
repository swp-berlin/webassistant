from typing import Protocol

from django.db.models.options import Options
from django.contrib.auth.models import PermissionsMixin


class HasMeta(Protocol):
    _meta: Options


# noinspection PyProtectedMember
def get_permission(obj: HasMeta, name: str):
    return f'{obj._meta.app_label}.{name}_{obj._meta.model_name}'


def has_perm(user: PermissionsMixin, obj: HasMeta, name: str):
    perm = get_permission(obj, name)

    return user.has_perm(perm)
