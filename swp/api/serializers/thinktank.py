from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from rest_framework.fields import BooleanField
from rest_framework.serializers import ModelSerializer

from swp.models import Thinktank, Pool

from .scraper import ScraperListSerializer


class BaseThinktankSerializer(ModelSerializer):
    """
    Base thinktank serializer.
    """

    can_manage = BooleanField(read_only=True)

    class Meta:
        model = Thinktank
        read_only_fields = [
            'can_manage',
            'last_run',
            'created',
            'publication_count',
            'scraper_count',
            'active_scraper_count',
            'last_error_count',
        ]
        fields = [
            'id',
            'pool',
            'name',
            'url',
            'is_active',
            'unique_fields',
            *read_only_fields,
        ]


class ThinktankSerializer(BaseThinktankSerializer):
    """
    Full thinktank serializer.
    """

    scrapers = ScraperListSerializer(many=True, read_only=True)
    is_active = BooleanField(label=_('active'), required=False)

    class Meta(BaseThinktankSerializer.Meta):
        read_only_fields = [*BaseThinktankSerializer.Meta.read_only_fields, 'scrapers']
        fields = [*BaseThinktankSerializer.Meta.fields, 'description', 'scrapers']

    def validate_pool(self, pool: Pool):
        if self.context.get('request').user.can_manage_pool(pool):
            return pool

        raise ValidationError(
            message=_('You cannot add thinktanks to pool %(pool)s.'),
            params={'pool': pool},
            code='no-manager',
        )


class ThinktankListSerializer(BaseThinktankSerializer):
    """
    Light serializer for thinktank lists.
    """

    class Meta(BaseThinktankSerializer.Meta):
        read_only_fields = [*BaseThinktankSerializer.Meta.read_only_fields, 'is_active']
