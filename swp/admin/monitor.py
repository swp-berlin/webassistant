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
        'created',
    ]
    readonly_fields = ['created']
    list_display = [
        'name',
        'created',
        'last_sent',
    ]
    list_filter = [
        'is_active',
        'last_sent',
        'created',
    ]
