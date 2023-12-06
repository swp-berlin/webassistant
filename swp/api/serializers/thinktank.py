from django.utils.translation import gettext_lazy as _

from rest_framework.fields import BooleanField
from rest_framework.serializers import ModelSerializer

from swp.models import Thinktank
from .scraper import ScraperListSerializer


class ThinktankSerializer(ModelSerializer):
    """
    Full thinktank serializer.
    """

    scrapers = ScraperListSerializer(many=True, read_only=True)

    is_active = BooleanField(label=_('Active'), required=False)

    class Meta:
        model = Thinktank
        read_only_fields = [
            'last_run',
            'created',
            'publication_count',
            'scraper_count',
            'active_scraper_count',
            'last_error_count',
            'scrapers',
        ]
        fields = [
            'id',
            'name',
            'description',
            'url',
            'unique_fields',
            'is_active',
            *read_only_fields,
        ]


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
            'active_scraper_count',
            'last_error_count',
        ]
        fields = [
            'id',
            'name',
            'url',
            'unique_fields',
            *read_only_fields,
        ]
