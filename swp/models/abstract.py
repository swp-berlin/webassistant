from __future__ import annotations

from django.contrib.auth import get_permission_codename
from django.contrib.auth.models import AbstractUser as User
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.db import models
from django.db.models.base import ModelBase
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from swp.utils.permission import has_perm


class UpdateQuerySet(models.QuerySet):
    """
    QuerySet for locking row during update.
    """

    def get_for_update(self, *, nowait: bool = False, **kwargs):
        return self.select_for_update(nowait=nowait).get(**kwargs)


class ActivatableQuerySet(UpdateQuerySet):
    """
    QuerySet for :class:`Activatable` models.
    """

    def active(self) -> ActivatableQuerySet:
        return self.filter(is_active=True)

    def inactive(self) -> ActivatableQuerySet:
        return self.filter(is_active=False)

    def activate(self):
        return self.update(is_active=True)

    activate.alters_data = True

    def deactivate(self):
        return self.update(is_active=False)

    deactivate.alters_data = True


class ActivatableManager(models.Manager.from_queryset(ActivatableQuerySet, 'BaseActivatableManager')):
    """
    Manager for :class:`Activatable` models.
    """
    use_in_migrations = True


class ActivatableModelBase(ModelBase):

    actions = ('activate', 'deactivate')

    def __new__(cls, name, bases, attrs, **kwargs):
        new_class = super().__new__(cls, name, bases, attrs, **kwargs)

        # Check if required permissions are set on model.
        if not new_class._meta.abstract:
            new_permissions = new_class._meta.permissions
            new_codenames = tuple(codename for codename, label in new_permissions)
            for action in cls.actions:
                if action in new_class._meta.default_permissions:
                    continue
                codename = get_permission_codename(action, new_class._meta)
                if codename not in new_codenames:
                    raise ImproperlyConfigured(_('Missing %s permission') % codename)

        return new_class


class ActivatableModel(models.Model, metaclass=ActivatableModelBase):
    """
    Mixin for (de)activatable models.
    """
    is_active = models.BooleanField(_('active'), default=False)

    objects = ActivatableManager()

    class Meta:
        abstract = True
        default_permissions = (
            'add',
            'change',
            'delete',
            'view',
            'activate',
            'deactivate',
        )

    def can_activate(self, user: User) -> bool:
        """ Check user for permission to activate. """

        return has_perm(user, self, 'activate')

    def can_deactivate(self, user: User) -> bool:
        """ Check user for permission to deactivate. """

        return has_perm(user, self, 'deactivate')

    def set_active(self, is_active: bool, *, commit: bool = True):
        self.is_active = is_active
        if commit:
            self.save(update_fields=['is_active'])

    def activate(self, user: User):
        """ Activate instance. """
        if not self.can_activate(user):
            raise PermissionDenied(_('Activation denied'))

        self.set_active(True)

    def deactivate(self, user: User):
        """ Deactivate instance. """
        if not self.can_deactivate(user):
            raise PermissionDenied(_('Deactivation denied'))

        self.set_active(False)


class UpdateQuerySet(models.QuerySet):

    def get_for_update(self, *, nowait=False, **kwargs):
        return self.select_for_update(nowait=nowait).get(**kwargs)


class LastModified(models.Model):
    created = models.DateTimeField(_('created'), default=timezone.now, editable=False)
    last_modified = models.DateTimeField(_('last modified'), auto_now=True)

    objects = UpdateQuerySet.as_manager()

    class Meta:
        abstract = True

    def update(self, *, using=None, modified: bool = True, **values):
        update_fields = {*values}

        if modified:
            update_fields.add('last_modified')

        for field, value in values.items():
            setattr(self, field, value)

        return self.save(update_fields=list(update_fields), using=using)
