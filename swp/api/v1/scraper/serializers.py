from rest_framework import serializers

from swp.api.v1.serializers import ActivatableSerializer
from swp.models import Scraper


class ScraperSerializer(ActivatableSerializer):

    class Meta:
        model = Scraper
        fields = serializers.ALL_FIELDS
