from django.contrib import admin

from swp.models import Monitor


@admin.register(Monitor)
class MonitorAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    fields = [
        'name',
        'recipients',
        'interval',
        'last_sent',
        'is_active',
        'created',
    ]
    readonly_fields = ['created']
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
