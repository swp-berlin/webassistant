from django.contrib import admin

from swp.models import Publication


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    fields = [
        'thinktank',
        'scrapers',
        'ris_type',
        'title',
        'subtitle',
        'authors',
        'abstract',
        'publication_date',
        'publication_dt',
        'last_access',
        'url',
        'pdf_url',
        'pdf_pages',
        'tags',
    ]
    readonly_fields = [
        'last_access',
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
    ]
