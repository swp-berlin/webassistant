import json

from rest_framework.fields import JSONField
from rest_framework.serializers import ModelSerializer

from swp.models import Scraper

from .thinktank import ThinktankSerializer


class ScraperSerializer(ModelSerializer):
    thinktank = ThinktankSerializer()
    data = JSONField()

    class Meta:
        model = Scraper
        fields = ['id', 'type', 'thinktank', 'is_active', 'data', 'start_url', 'interval', 'last_run']

    def save(self, **kwargs):
        return super().save(data=json.loads(self.validated_data.get('data')))
