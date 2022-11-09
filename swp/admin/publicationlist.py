from django.contrib import admin
from django.db import models
from django.db.models.functions import Greatest
from django.utils.translation import gettext_lazy as _

from swp.models import PublicationList, PublicationListEntry

from .base import DefaultTabularInline


class PublicationListEntryInlineAdmin(DefaultTabularInline):
    model = PublicationListEntry
    raw_id_fields = ['publication']
    readonly_fields = ['created']


@admin.register(PublicationList)
class PublicationListAdmin(admin.ModelAdmin):
    inlines = [PublicationListEntryInlineAdmin]
    list_display = ['user', 'name', 'entry_count', 'last_updated']
    raw_id_fields = ['user']

    def get_queryset(self, request):
        return super(PublicationListAdmin, self).get_queryset(request).annotate(
            entry_count=models.Count('entries'),
            last_updated=Greatest(
                models.F('last_modified'),
                models.Max('entries__created'),
            ),
        )

    @admin.display(description=_('# Entries'), ordering='entry_count')
    def entry_count(self, obj: PublicationList):
        return obj.entry_count

    @admin.display(description=_('Last Updated'), ordering='last_updated')
    def last_updated(self, obj: PublicationList):
        return obj.last_updated
