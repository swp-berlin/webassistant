from django.contrib import admin

from swp.models import Thinktank
from .abstract import ActivatableModelAdmin


@admin.register(Thinktank)
class ThinktankAdmin(ActivatableModelAdmin):
    date_hierarchy = 'created'
    fields = [
        'name',
        'description',
        'url',
        'unique_fields',
        'is_active',
        'created',
    ]
    readonly_fields = ['created']
    list_display = [
        'name',
        'url',
        'created',
        'is_active',
    ]
    list_filter = [
        'is_active',
        'created',
    ]
