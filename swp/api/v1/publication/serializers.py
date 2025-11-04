from django.db.models import Prefetch
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from swp.models import Publication, Scraper, Thinktank

SCRAPERS = Scraper.objects.prefetch_related(
    Prefetch('thinktank', Thinktank.objects.only('name')),
)


class PublicationSerializer(ModelSerializer):

    class Meta:
        model = Publication
        fields = serializers.ALL_FIELDS
        extra_kwargs = {
            'scrapers': {
                'queryset': SCRAPERS,
            },
        }
