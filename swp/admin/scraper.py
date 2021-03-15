from django.contrib import admin

from swp.models import Scraper, ScraperError
from .abstract import ActivatableModelAdmin


class ScraperErrorInline(admin.StackedInline):
    model = ScraperError
    readonly_fields = ['publication']
    fields = [
        'publication',
        'message',
        'field',
        'code',
    ]


@admin.register(Scraper)
class ScraperAdmin(ActivatableModelAdmin):
    date_hierarchy = 'created'
    fields = [
        'thinktank',
        'type',
        'data',
        'start_url',
        'checksum',
        'interval',
        'last_run',
        'is_active',
        'created',
    ]
    readonly_fields = ['created', 'last_run']
    list_display = [
        'thinktank',
        'type',
        'start_url',
        'checksum',
        'last_run',
        'is_active',
    ]
    list_filter = [
        'is_active',
        'interval',
        'last_run',
    ]
    search_fields = [
        'checksum',
        'thinktank__name',
    ]

    inlines = [
        ScraperErrorInline,
    ]
