from django import forms
from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _, ngettext

from swp.models import Monitor
from .abstract import ActivatableModelAdmin
from swp.tasks.monitor import send_publications_to_zotero


class MonitorAdminForm(forms.ModelForm):

    class Meta:
        model = Monitor
        fields = [
            'name',
            'description',
            'recipients',
            'zotero_keys',
            'interval',
            'is_active',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['zotero_keys'].widget.attrs['size'] = 100


@admin.register(Monitor)
class MonitorAdmin(ActivatableModelAdmin):
    date_hierarchy = 'created'
    form = MonitorAdminForm
    fields = [
        'name',
        'description',
        'recipients',
        'zotero_keys',
        'interval',
        'last_sent',
        'is_active',
        'created',
    ]
    readonly_fields = ['created', 'last_sent']
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
    actions = ['send_to_zotero']

    def send_to_zotero(self, request, queryset):
        for monitor in queryset:
            send_publications_to_zotero.delay(monitor.pk)

        monitor_count = len(queryset)

        self.message_user(request, ngettext(
            'Publications for %d monitor will be transferred to zotero',
            'Publications for %d monitors will be transferred to zotero',
            monitor_count,
        ) % monitor_count, messages.SUCCESS)
    send_to_zotero.short_description = _('Send publications for selected monitors to zotero')
