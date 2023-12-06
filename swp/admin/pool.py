from urllib.parse import urlencode

from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from swp.models import Pool, Thinktank
from swp.utils.admin import DEFAULT_LINK_TEMPLATE, admin_url


@admin.register(Pool)
class PoolAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'thinktank_count', 'created']
    list_display_links = ['name']

    def get_queryset(self, request):
        return admin.ModelAdmin.get_queryset(self, request).annotate(
            thinktank_count=models.Count('thinktanks'),
        )

    @admin.display(description=_('# thinktanks'), ordering='thinktank_count')
    def thinktank_count(self, obj: Pool):
        url = admin_url(Thinktank, 'changelist', site=self.admin_site)
        params = urlencode({'pool__id__exact': obj.id})

        return format_html(DEFAULT_LINK_TEMPLATE, url=f'{url}?{params}', label=obj.thinktank_count)


class CanManagePermissionMixin:

    def has_manage_permission(self, perm: str, request, obj=None):
        if getattr(super(), f'has_{perm}_permission')(request, obj=obj):
            return obj is None or self.can_manage_pool(request, obj)

        return False

    def has_change_permission(self, request, obj=None):
        return self.has_manage_permission('change', request, obj=obj)

    def has_delete_permission(self, request, obj=None):
        return self.has_manage_permission('delete', request, obj=obj)

    def can_manage_pool(self, request, obj):
        raise NotImplementedError
