from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from swp.models import Scraper


class ScraperSerializer(ModelSerializer):

    class Meta:
        model = Scraper
        fields = serializers.ALL_FIELDS
