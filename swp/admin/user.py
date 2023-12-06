from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from swp.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    date_hierarchy = 'date_joined'
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Notifications'), {'fields': ('is_error_recipient',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'pools'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    filter_horizontal = [*BaseUserAdmin.filter_horizontal, 'pools']
    list_display = [
        'email',
        'first_name',
        'last_name',
        'last_login',
        'is_staff',
        'is_active',
    ]
    list_filter = [
        'is_error_recipient',
        'is_active',
        'last_login',
    ]
    ordering = ['email']
    readonly_fields = ['date_joined', 'last_login']
    search_fields = [
        'email',
        'first_name',
        'last_name',
    ]
