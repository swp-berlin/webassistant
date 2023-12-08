from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from swp.models import Thinktank

from .abstract import ActivatableModelAdmin
from .pool import CanManagePermissionMixin


@admin.register(Thinktank)
class ThinktankAdmin(CanManagePermissionMixin, ActivatableModelAdmin):
    date_hierarchy = 'created'
    fields = [
        'pool',
        'domain',
        'name',
        'description',
        'url',
        'unique_fields',
        'is_active',
        'created',
    ]
    readonly_fields = ['created']
    list_select_related = []
    list_display = [
        'name',
        'url_display',
        'pool',
        'domain',
        'created',
        'is_active',
    ]
    list_filter = [
        'is_active',
        'pool',
        'created',
    ]

    def get_queryset(self, request):
        return ActivatableModelAdmin.get_queryset(self, request).prefetch_related('pool')

    @admin.display(description=_('URL'), ordering='url')
    def url_display(self, obj: Thinktank):
        return format_html('<a href="{url}" target="_blank">{url}</a>', url=obj.url)

    def can_manage_pool(self, request, obj: Thinktank):
        return request.user.can_manage_pool(obj.pool)
