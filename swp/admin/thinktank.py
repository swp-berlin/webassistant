from django.contrib import admin

from swp.models import Thinktank


@admin.register(Thinktank)
class ThinktankAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    fields = [
        'name',
        'description',
        'url',
        'unique_field',
    ]
    list_display = [
        'name',
        'url',
        'created',
    ]
