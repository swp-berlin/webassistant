from django.utils.translation import gettext_lazy as _

from django_filters import rest_framework as filters

from swp.api.v1.filters import SWPFilterSet
from swp.models import Pool, Scraper


class ScraperFilterSet(SWPFilterSet):
    pool = filters.ModelChoiceFilter('thinktank__pool', label=_('pool'), queryset=Pool.objects)

    class Meta:
        model = Scraper
        fields = [
            'name',
            'pool',
            'start_url',
            'is_active',
        ]
