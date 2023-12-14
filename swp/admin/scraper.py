from functools import wraps

from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _, ngettext

from swp.models import Scraper, ScraperError
from swp.utils.domain import is_subdomain

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

    @wraps(ActivatableModelAdmin.activate)
    def activate(self, request, queryset):
        scrapers = queryset.values_list('id', 'start_url', 'thinktank__domain')
        incompatible = [scraper for scraper, url, domain in scrapers if not is_subdomain(url, domain)]

        if count := len(incompatible):
            queryset = queryset.exclude(id__in=incompatible)
            message = ngettext(
                "%(count)s scraper could not be activated because its start "
                "url is not a subdomain of its thinktank's domain.",
                "%(count)s scrapers could not be activated because their start "
                "url is not a subdomain of their thinktank's domain.",
                count,
            )

            self.message_user(request, message % {'count': count}, messages.WARNING)

        return super().activate(request, queryset)
