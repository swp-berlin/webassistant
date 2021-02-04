from django.contrib import admin

from swp.models import PublicationFilter, ThinktankFilter


class PublicationFilterInline(admin.TabularInline):
    model = PublicationFilter
    extra = 1


@admin.register(ThinktankFilter)
class ThinktankFilterAdmin(admin.ModelAdmin):
    fields = [
        'monitor',
        'thinktank',
    ]
    list_display = [
        'monitor',
        'thinktank',
    ]
    inlines = [
        PublicationFilterInline,
    ]
