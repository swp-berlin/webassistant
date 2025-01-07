from django.contrib import admin

from swp.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ['last_modified', 'created']
    list_display = ['name', *readonly_fields]
    search_fields = ['name']

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields if obj else []
