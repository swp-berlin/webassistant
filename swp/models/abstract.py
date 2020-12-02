from __future__ import annotations

from django.contrib.auth import get_permission_codename
from django.contrib.auth.models import AbstractUser as User
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models.base import ModelBase
from django.utils.translation import gettext_lazy as _


class ActivatableQuerySet(models.QuerySet):
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
    is_active = models.BooleanField(_('active'), default=True)

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
        return user.has_perm(get_permission_codename('activate', self._meta))

    def can_deactivate(self, user: User) -> bool:
        """ Check user for permission to deactivate. """
        return user.has_perm(get_permission_codename('deactivate', self._meta))

    def set_active(self, is_active: bool, *, commit: bool = True):
        self.is_active = is_active
        if commit:
            self.save(update_fields=['is_active'])

    def activate(self, user: User):
        """ Activate instance. """
        assert self.can_activate(user), _('Activation denied')

        self.set_active(True)

    def deactivate(self, user: User):
        """ Deactivate instance. """
        assert self.can_deactivate(user), _('Deactivation denied')

        self.set_active(False)
