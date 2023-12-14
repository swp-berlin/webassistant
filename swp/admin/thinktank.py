from functools import wraps

from django.contrib import admin, messages
from django.db import models, transaction
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _, ngettext

from swp.models import Thinktank
from swp.utils.text import enumeration

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

    @transaction.atomic
    def save_model(self, request, obj: Thinktank, form, change):
        if change and obj.is_active and {'domain', 'is_active'} & {*form.changed_data}:
            self.deactivate_incompatible_scrapers(request, obj)

        obj.save()

    def deactivate_incompatible_scrapers(self, request, obj: Thinktank):
        if count := obj.deactivate_incompatible_scrapers():
            message = ngettext(
                'Deactivated %(count)s scraper because its start url is not a subdomain of %(domain)s.',
                'Deactivated %(count)s scrapers because their start url is not a subdomain of %(domain)s.',
                count,
            )

            self.message_user(request, message % {'count': count, 'domain': obj.domain}, messages.WARNING)

    @transaction.atomic
    @wraps(ActivatableModelAdmin.activate)
    def activate(self, request, queryset):
        duplicates = queryset.filter(
            models.Exists(
                Thinktank.objects.exclude(
                    id=models.OuterRef('id'),
                ).filter(
                    domain=models.OuterRef('domain'),
                    is_active=True,
                ),
            ),
        )

        if domains := duplicates.values_list('domain', flat=True):
            message = ngettext(
                'Could not activate selected thinktanks because the following domain is duplicated: %(domains)s',
                'Could not activate selected thinktanks because the following domains are duplicated: %(domains)s',
                len(domains),
            )
            domains = enumeration(domains)

            return self.message_user(request, message % {'domains': domains}, messages.ERROR)

        super().activate(request, queryset)

        count = 0

        for thinktank in queryset.only('domain'):
            count += thinktank.deactivate_incompatible_scrapers()

        if count:
            message = ngettext(
                "Deactivated %(count)s scraper because its start url "
                "is not a subdomain of its thinktank's domain.",
                "Deactivated %(count)s scrapers because their start url "
                "is not a subdomain of their thinktank's domain.",
                count,
            )

            self.message_user(request, message % {'count': count}, messages.WARNING)
