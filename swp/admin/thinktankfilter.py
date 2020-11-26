from django.contrib import admin

from swp.models import ThinktankFilter


@admin.register(ThinktankFilter)
class ThinktankFilterAdmin(admin.ModelAdmin):
    fields = [
        'monitor',
        'thinktank',
        'query',
    ]
    list_display = [
        'monitor',
        'thinktank',
    ]
