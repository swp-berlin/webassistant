from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from swp.models import ScraperError


class ScraperErrorSerializer(ModelSerializer):

    class Meta:
        model = ScraperError
        fields = serializers.ALL_FIELDS
