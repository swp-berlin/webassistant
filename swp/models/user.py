from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.contrib.postgres.fields import CIEmailField
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from swp.utils.translation import trans


class UserManager(DjangoUserManager):

    def create_user(self, username=None, email=None, password=None, **extra_fields):
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

    is_error_recipient = models.BooleanField(_('is error recipient'), default=False)

    pools = models.ManyToManyField('swp.Pool', verbose_name=_('pools'), related_name='users', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ()

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        pass

    @property
    def username(self):
        return self.email

    @property
    def can_research(self):
        return self.has_perm(f'{self._meta.app_label}.can_research')

    @cached_property
    def has_pools(self):
        return self.pools.exists()

    def can_manage_pool(self, pool):
        return self.pools.filter(id=pool.id).exists() if self.has_pools else True
