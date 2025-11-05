from django.contrib import admin

from swp.models import AuthToken


@admin.register(AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    list_display = fields = ['user', 'key', 'expires', 'created', 'last_modified']
    readonly_fields = ['user', 'key', 'created', 'last_modified']
    add_fields = ['user', 'expires']
    raw_id_fields = ['user']
    search_fields = ['key', 'user__email', 'user__first_name', 'user__last_name']

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields if obj else []

    def get_fields(self, request, obj=None):
        return self.fields if obj else self.add_fields
