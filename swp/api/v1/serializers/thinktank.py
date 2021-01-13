from django.utils.translation import gettext_lazy as _

from rest_framework.fields import BooleanField
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from swp.models import Thinktank
from .scraper import ScraperListSerializer


class ThinktankSerializer(ModelSerializer):
    """
    Full thinktank serializer.
    """

    scraper_count = SerializerMethodField()
    last_error_count = SerializerMethodField()
    scrapers = ScraperListSerializer(many=True, read_only=True)

    is_active = BooleanField(label=_('Active'), required=False)

    class Meta:
        model = Thinktank
        read_only_fields = [
            'last_run',
            'created',
            'publication_count',
            'scraper_count',
            'last_error_count',
            'scrapers',
        ]
        fields = [
            'id',
            'name',
            'description',
            'url',
            'unique_field',
            'is_active',
            *read_only_fields,
        ]

    def get_scraper_count(self, obj: Thinktank) -> int:
        return sum(1 for scraper in obj.scrapers.all())

    def get_last_scraper(self, obj: Thinktank):
        scrapers = [scraper for scraper in obj.scrapers.all() if scraper.last_run is not None]
        latest = None
        for scraper in scrapers:
            last_run = getattr(latest, 'last_run', None)
            if last_run is None or scraper.last_run > last_run:
                latest = scraper

        return latest

    def get_last_error_count(self, obj: Thinktank) -> int:
        return getattr(self.get_last_scraper(obj), 'error_count', 0)


class ThinktankListSerializer(ModelSerializer):
    """
    Light serializer for thinktank lists.
    """

    class Meta:
        model = Thinktank
        read_only_fields = [
            'is_active',
            'last_run',
            'created',
            'publication_count',
            'scraper_count',
            'last_error_count',
        ]
        fields = [
            'id',
            'name',
            'url',
            'unique_field',
            *read_only_fields,
        ]
