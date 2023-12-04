from urllib.parse import urlencode

from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from swp.models import Pool, Thinktank
from swp.utils.admin import DEFAULT_LINK_TEMPLATE, admin_url


@admin.register(Pool)
class PoolAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'thinktank_count', 'created']
    list_display_links = ['name']

    def get_queryset(self, request):
        return admin.ModelAdmin.get_queryset(self, request).annotate(
            thinktank_count=models.Count('thinktanks'),
        )

    @admin.display(description=_('# thinktanks'), ordering='thinktank_count')
    def thinktank_count(self, obj: Pool):
        url = admin_url(Thinktank, 'changelist', site=self.admin_site)
        params = urlencode({'pool__id__exact': obj.id})

        return format_html(DEFAULT_LINK_TEMPLATE, url=f'{url}?{params}', label=obj.thinktank_count)
