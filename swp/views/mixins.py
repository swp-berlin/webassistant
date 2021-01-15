from __future__ import annotations
from typing import Any, Mapping, TYPE_CHECKING

from swp.api.v1.serializers import UserSerializer
if TYPE_CHECKING:
    from django.contrib.auth.base_user import AbstractBaseUser as User
    from rest_framework.serializers import ModelSerializer


class UserDataMixin:
    """
    Mixin for serialized data of current user.
    """

    user_serializer_class = UserSerializer
    context_user_data_name = 'user_data'

    def get_user_serializer(self, *args, **kwargs) -> ModelSerializer:
        return self.user_serializer_class(*args, **kwargs)

    def get_user_data(self, user: User = None, **kwargs) -> Mapping[str, Any]:
        instance = self.request.user if user is None else user
        serializer = self.get_user_serializer(instance, **kwargs)

        return serializer.data

    def get_context_data(self, **kwargs) -> Mapping[str, Any]:
        context = {
            self.context_user_data_name: self.get_user_data(),
        }

        return super().get_context_data(**context, **kwargs)
