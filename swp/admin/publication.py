from django.contrib import admin

from swp.models import Publication


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    pollux_fields = Publication.POLLUX_FIELDS
    readonly_fields = [
        'last_access',
        *pollux_fields,
    ]
    fields = [
        'thinktank',
        'scrapers',
        'ris_type',
        'title',
        'subtitle',
        'authors',
        'abstract',
        'publication_date',
        'url',
        'pdf_url',
        'pdf_pages',
        'tags',
        'categories',
        *readonly_fields,
    ]
    raw_id_fields = [
        'thinktank',
        'scrapers',
    ]
    autocomplete_fields = [
        'categories',
    ]
    list_display = [
        'title',
        'thinktank',
        'last_access',
    ]
    list_filter = [
        'thinktank',
        'ris_type',
        'last_access',
    ]
    search_fields = [
        'title',
        'subtitle',
        'abstract',
        'tags',
        'categories__name',
    ]
