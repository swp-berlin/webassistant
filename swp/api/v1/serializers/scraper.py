from rest_framework.serializers import ModelSerializer

from swp.models import Scraper

from .thinktank import ThinktankSerializer


class ScraperSerializer(ModelSerializer):
    thinktank = ThinktankSerializer()

    class Meta:
        model = Scraper
        fields = ['id', 'type', 'thinktank', 'is_active', 'data', 'start_url', 'interval', 'last_run']
