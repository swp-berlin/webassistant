from __future__ import annotations

from django.db import models
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


class ActivatableModel(models.Model):
    """
    Mixin for (de)activatable models.
    """
    is_active = models.BooleanField(_('active'), default=True)

    objects = ActivatableManager()

    class Meta:
        abstract = True
