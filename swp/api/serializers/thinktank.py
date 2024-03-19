from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from rest_framework.fields import BooleanField, IntegerField
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
    deactivated_scrapers = IntegerField(read_only=True, default=0)

    class Meta(BaseThinktankSerializer.Meta):
        read_only_fields = [*BaseThinktankSerializer.Meta.read_only_fields, 'scrapers', 'deactivated_scrapers']
        fields = [*BaseThinktankSerializer.Meta.fields, 'domain', 'description', 'scrapers', 'deactivated_scrapers']

    def validate_pool(self, pool: Pool):
        if self.context.get('request').user.can_manage_pool(pool):
            return pool

        raise ValidationError(
            message=_('You are not authorized to add thinktanks to pool %(pool)s.'),
            params={'pool': pool},
            code='no-manager',
        )

    def validate(self, attrs):
        self.validate_unique_domain(attrs)

        return attrs

    def validate_unique_domain(self, attrs):
        if instance := self.instance:
            is_active = attrs.get('is_active', instance.is_active)
            domain = attrs.get('domain', instance.domain)
            exclude = instance.id
        else:
            is_active = attrs.get('is_active', True)
            domain = attrs.get('domain', '')
            exclude = None

        if is_active:
            Thinktank.validate_unique_domain(domain, exclude)

    @transaction.atomic
    def update(self, instance: Thinktank, validated_data):
        should_deactivate_incompatible_scrapers = self.should_deactivate_incompatible_scrapers(instance, validated_data)
        instance = super().update(instance, validated_data)

        if should_deactivate_incompatible_scrapers:
            instance.deactivated_scrapers = instance.deactivate_incompatible_scrapers()

        return instance

    @staticmethod
    def should_deactivate_incompatible_scrapers(instance, validated_data):
        if validated_data.get('is_active'):
            return True

        if validated_data.get('is_active', instance.is_active):
            return not instance.domain == validated_data.get('domain', instance.domain)

        return False


class ThinktankListSerializer(BaseThinktankSerializer):
    """
    Light serializer for thinktank lists.
    """

    class Meta(BaseThinktankSerializer.Meta):
        read_only_fields = [*BaseThinktankSerializer.Meta.read_only_fields, 'is_active']
