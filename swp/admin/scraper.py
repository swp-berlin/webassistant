from django.contrib import admin

from swp.models import Scraper


@admin.register(Scraper)
class ScraperAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    fields = [
        'thinktank',
        'type',
        'data',
        'start_url',
        'checksum',
        'interval',
        'last_run',
        'created',
    ]
    readonly_fields = ['created']
    list_display = [
        'thinktank',
        'type',
        'start_url',
        'checksum',
        'last_run',
    ]
    list_filter = [
        'is_active',
        'last_run',
    ]
    search_fields = [
        'checksum',
        'thinktank__name',
    ]
