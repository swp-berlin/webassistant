from django.db.models import Prefetch

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from swp.api.v1.serializers import ReadOnlyMixin
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


class PublicationSearchSerializer(ReadOnlyMixin, PublicationSerializer):
    """
    Special serializer for search that does not prefill the browsable api's content field.
    """
