from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.contrib.postgres.fields import CIEmailField

from cosmogo.utils.gettext import trans


class UserManager(DjangoUserManager):

    def create_user(self, username, email=None, password=None, **extra_fields):
        return super().create_user(email, email=email, password=password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        return super().create_superuser(email, email=email, password=password, **extra_fields)

    def _create_user(self, username, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractUser):
    email = CIEmailField(trans('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ()

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        pass

    @property
    def username(self):
        return self.email
