from django import forms
from django.contrib import admin

from swp.models import Monitor
from .abstract import ActivatableModelAdmin


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
