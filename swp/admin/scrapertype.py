from django.contrib import admin

from swp.models import ScraperType


@admin.register(ScraperType)
class ScraperTypeAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'config',
    ]
