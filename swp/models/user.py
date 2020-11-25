from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.contrib.postgres.fields import CIEmailField

from cosmogo.utils.gettext import trans


class UserManager(DjangoUserManager):

    def _create_user(self, email, password, **extra_fields):
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
