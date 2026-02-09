from django.utils.translation import gettext_lazy as _

from django_filters import rest_framework as filters

from swp.api.v1.publication.serializers import SCRAPERS
from swp.models import ScraperError


class ScraperErrorFilterSet(filters.FilterSet):
    scraper = filters.ModelChoiceFilter(label=_('scraper'), queryset=SCRAPERS)

    class Meta:
        model = ScraperError
        fields = [
            'level',
            'scraper',
        ]
