from typing import Union

from django.contrib import admin, messages
from django.contrib.auth import get_permission_codename
from django.db import models
from django.db.models.base import ModelBase
from django.utils.translation import gettext_lazy as _, ngettext

from swp.models import ActivatableModel


def get_pluralized_verbose_name(model: Union[models.Model, ModelBase], count: int = 1) -> str:
    """ Choose singular or plural model name, depending on count. """
    return ngettext(model._meta.verbose_name, model._meta.verbose_name_plural, count)


class BaseActivatableModelAdmin(admin.ModelAdmin):

    def get_permission_name(self, action):
        return f'{self.opts.app_label}.%s' % get_permission_codename(action, self.opts)

    @property
    def activate_permission_name(self):
        return self.get_permission_name('activate')

    @property
    def deactivate_permission_name(self):
        return self.get_permission_name('deactivate')

    def can_activate(self, request) -> bool:
        return request.user.has_perm(self.activate_permission_name)

    def can_deactivate(self, request) -> bool:
        return request.user.has_perm(self.deactivate_permission_name)

    def can_toggle_active(self, request, obj: ActivatableModel):
        return self.can_deactivate(request) if obj.is_active else self.can_activate(request)

    def has_activate_permission(self, request, obj: ActivatableModel = None) -> bool:
        raise NotImplementedError

    def has_deactivate_permission(self, request, obj: ActivatableModel = None) -> bool:
        raise NotImplementedError


class ActivatableModelAdmin(BaseActivatableModelAdmin):
    """
    Base admin for :class:`~swp.models.abstract.ActivatableModel` models.
    """

    def has_activate_permission(self, request, obj=None):
        return self.can_activate(request)

    def has_deactivate_permission(self, request, obj=None):
        return self.can_deactivate(request)

    # <editor-fold desc="Actions">

    actions = ['activate', 'deactivate']

    def toggle_message(self, request, message, count):
        name = get_pluralized_verbose_name(self.model, count)
        context = {'count': count, 'name': name}
        level = messages.SUCCESS if count else messages.WARNING

        self.message_user(request, message % context, level)

    def activate(self, request, queryset):
        return self.toggle_message(request, _('Activated %(count)d %(name)s.'), queryset.activate())

    activate.short_description = _('Activate selected %(verbose_name_plural)s')
    activate.allowed_permissions = ['activate']

    def deactivate(self, request, queryset):
        return self.toggle_message(request, _('Deactivated %(count)d %(name)s.'), queryset.deactivate())

    deactivate.short_description = _('Deactivate selected %(verbose_name_plural)s')
    activate.allowed_permissions = ['deactivate']

    # </editor-fold>

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj=obj)

        if obj is None or self.can_toggle_active(request, obj):
            return readonly_fields

        return [*readonly_fields, 'is_active']
