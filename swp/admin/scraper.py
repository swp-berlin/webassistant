from functools import wraps

from django.contrib import admin, messages
from django.db.models import Prefetch
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _, ngettext

from swp.models import Publication, Scraper, ScraperError
from swp.utils.admin import DEFAULT_LINK_TEMPLATE
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

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            Prefetch('publication', Publication.objects.only('title')),
        )


@admin.register(Scraper)
class ScraperAdmin(CanManagePermissionMixin, ActivatableModelAdmin):
    date_hierarchy = 'created'
    fields = [
        'thinktank',
        'type',
        'categories',
        'data',
        'start_url',
        'checksum',
        'interval',
        'is_active',
        'is_running',
        'last_run',
        'created',
    ]
    raw_id_fields = [
        'thinktank',
    ]
    autocomplete_fields = [
        'categories',
    ]
    readonly_fields = [
        'created',
        'last_run',
        'is_running',
    ]
    list_select_related = []
    list_display = [
        'thinktank',
        'pool_display',
        'type',
        'start_url_display',
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

    @admin.display(description=_('start URL'), ordering='start_url')
    def start_url_display(self, obj: Scraper):
        return format_html(DEFAULT_LINK_TEMPLATE, url=obj.start_url, label=obj.start_url)

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
