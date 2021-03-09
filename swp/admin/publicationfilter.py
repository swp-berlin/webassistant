from django.contrib import admin

from swp.models import PublicationFilter


@admin.register(PublicationFilter)
class PublicationFilterAdmin(admin.ModelAdmin):
    fields = [
        'thinktank_filter',
        'field',
        'comparator',
        'value',
    ]
