from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from swp.models import Scraper, ScraperError

from .abstract import ActivatableModelAdmin
from .pool import CanManagePermissionMixin


class ScraperErrorInline(admin.StackedInline):
    model = ScraperError
    readonly_fields = ['publication']
    extra = 0
    fields = [
        'publication',
        'message',
        'field',
        'code',
    ]


@admin.register(Scraper)
class ScraperAdmin(CanManagePermissionMixin, ActivatableModelAdmin):
    date_hierarchy = 'created'
    fields = [
        'thinktank',
        'type',
        'data',
        'start_url',
        'checksum',
        'interval',
        'last_run',
        'is_running',
        'is_active',
        'created',
    ]
    readonly_fields = ['created', 'last_run', 'is_running']
    list_select_related = []
    list_display = [
        'thinktank',
        'pool_display',
        'type',
        'start_url',
        'checksum',
        'last_run',
        'is_active',
        'is_running',
    ]
    list_filter = [
        'is_active',
        'thinktank__pool',
        'interval',
        'last_run',
        'is_running',
    ]
    search_fields = [
        'checksum',
        'thinktank__name',
    ]

    inlines = [
        ScraperErrorInline,
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('thinktank__pool')

    @admin.display(description=_('pool'), ordering='thinktank__pool')
    def pool_display(self, obj: Scraper):
        return obj.thinktank.pool

    def can_manage_pool(self, request, obj: Scraper):
        return request.user.can_manage_pool(obj.thinktank.pool)
