from typing import Union

from django.contrib import admin
from django.contrib.auth import get_permission_codename
from django.db import models
from django.db.models.base import ModelBase
from django.utils.translation import gettext_lazy as _, ngettext


def get_pluralized_verbose_name(model: Union[models.Model, ModelBase], count: int = 1) -> str:
    """ Choose singular or plural model name, depending on count. """
    return ngettext(model._meta.verbose_name, model._meta.verbose_name_plural, count)


class ActivatableModelAdmin(admin.ModelAdmin):
    """
    Base admin for :class:`~swp.models.abstract.ActivatableModel` models.
    """

    def can_activate(self, request) -> bool:
        codename = get_permission_codename('activate', self.opts)
        return request.user.has_perm(f'{self.opts.app_label}.{codename}')

    def can_deactivate(self, request) -> bool:
        codename = get_permission_codename('deactivate', self.opts)
        return request.user.has_perm(f'{self.opts.app_label}.{codename}')

    # <editor-fold desc="Actions">

    actions = ['activate', 'deactivate']

    def activate(self, request, queryset):
        assert self.can_activate(request)
        count = queryset.activate()

        format_kwargs = {'count': count, 'name': get_pluralized_verbose_name(self.model, count)}
        self.message_user(request, _('Activated %(count)d %(name)s') % format_kwargs)

    activate.short_description = _('Activate selected %(verbose_name_plural)s')

    def deactivate(self, request, queryset):
        assert self.can_deactivate(request)
        count = queryset.deactivate()

        format_kwargs = {'count': count, 'name': get_pluralized_verbose_name(self.model, count)}
        self.message_user(request, _('Deactivated %(count)d %(name)s') % format_kwargs)

    deactivate.short_description = _('Deactivate selected %(verbose_name_plural)s')

    def get_actions(self, request):
        actions = super().get_actions(request)

        if not self.can_activate(request):
            actions.pop('activate', None)

        if not self.can_deactivate(request):
            actions.pop('deactivate', None)

        return actions

    # </editor-fold>

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj=obj))
        can_activate = self.can_activate(request)
        can_deactivate = self.can_deactivate(request)

        if not (can_activate and can_deactivate):
            is_active = getattr(obj, 'is_active', None)
            if is_active is False and not can_activate or is_active is True and not can_deactivate:
                readonly_fields.append('is_active')

        return readonly_fields
