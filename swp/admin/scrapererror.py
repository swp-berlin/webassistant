from django.contrib import admin

from swp.models import ScraperError


@admin.register(ScraperError)
class ScraperErrorAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    fields = [
        'scraper',
        'message',
        'code',
        'timestamp',
    ]
    readonly_fields = ['timestamp']
    list_display = [
        'scraper',
        'code',
        'message',
        'timestamp',
    ]
    list_filter = [
        'code',
    ]
    search_fields = [
        'code',
        'message',
    ]
