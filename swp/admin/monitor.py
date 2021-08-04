from django.contrib import admin

from swp.models import Monitor
from .abstract import ActivatableModelAdmin


@admin.register(Monitor)
class MonitorAdmin(ActivatableModelAdmin):
    date_hierarchy = 'created'
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

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['zotero_keys'].widget.attrs['size'] = 100

        return form
