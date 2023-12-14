from functools import wraps

from django import forms
from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _, ngettext

from swp.models import Monitor
from swp.tasks.monitor import send_publications_to_zotero

from .abstract import ActivatableModelAdmin


class MonitorAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in 'recipients', 'zotero_keys':
            if field := self.fields.get(field):
                field.widget.attrs['size'] = 100


@admin.register(Monitor)
class MonitorAdmin(ActivatableModelAdmin):
    date_hierarchy = 'created'
    form = MonitorAdminForm
    readonly_fields = ['last_sent', 'created']
    fields = [
        'name',
        'description',
        'query',
        'recipients',
        'zotero_keys',
        'interval',
        'is_active',
        *readonly_fields,
    ]
    list_display = [
        'name',
        'created',
        'last_sent',
        'is_active',
    ]
    list_filter = [
        'is_active',
        'interval',
        'last_sent',
        'created',
    ]
    actions = [*ActivatableModelAdmin.actions, 'send_to_zotero']

    def send_to_zotero(self, request, queryset):
        for monitor in queryset:
            send_publications_to_zotero.delay(monitor.pk)

        monitor_count = len(queryset)
        message = ngettext(
            'Publications for %d monitor will be transferred to zotero',
            'Publications for %d monitors will be transferred to zotero',
            monitor_count,
        )

        self.message_user(request, message % monitor_count, messages.SUCCESS)

    send_to_zotero.short_description = _('Send publications for selected monitors to zotero')

    @wraps(ActivatableModelAdmin.activate)
    def activate(self, request, queryset):
        if count := queryset.filter(query='').count():
            message = ngettext(
                '%(count)s monitor could not be activated because it has an empty query.',
                '%(count)s monitors could not be activated because they have empty queries.',
                count,
            )

            self.message_user(request, message % {'count': count}, messages.WARNING)

        queryset = queryset.exclude(query='')

        return super().activate(request, queryset)
