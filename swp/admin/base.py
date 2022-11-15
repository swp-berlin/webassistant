from django.contrib import admin


class DefaultTabularInline(admin.TabularInline):
    template = 'admin/inline/tabular-without-original.html'
    extra = 0
