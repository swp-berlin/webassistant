from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser as User


def create_superuser(email: str = 'admin@localhost', **kwargs) -> User:
    return get_user_model().objects.create_superuser(email, **kwargs)
