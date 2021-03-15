from rest_framework import serializers

from swp.models import ScraperError
from .fields import PublicationField


class ScraperErrorSerializer(serializers.ModelSerializer):
    publication = PublicationField()

    class Meta:
        model = ScraperError
        fields = [
            'id',
            'scraper',
            'identifier',
            'publication',
            'code',
            'level',
            'message',
            'field',
            'timestamp',
        ]
