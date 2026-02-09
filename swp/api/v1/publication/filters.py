from django.utils.translation import gettext_lazy as _

from django_filters import rest_framework as filters

from swp.models import Publication, Pool, Category

from .serializers import SCRAPERS


class PublicationFilterSet(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains', label=_('title'))
    pool = filters.ModelChoiceFilter('thinktank__pool', label=_('pool'), queryset=Pool.objects)
    scraper = filters.ModelChoiceFilter('scrapers', label=_('scraper'), queryset=SCRAPERS)
    category = filters.ModelChoiceFilter('categories', label=_('category'), queryset=Category.objects)

    class Meta:
        model = Publication
        fields = [
            'title',
            'pool',
            'thinktank',
            'scraper',
            'category',
        ]
