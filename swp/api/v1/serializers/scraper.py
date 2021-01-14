from collections import OrderedDict

from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, ChoiceField, IntegerField
from rest_framework.serializers import ModelSerializer, Serializer

from swp.models import Scraper
from swp.models.choices import DataResolverKey, ResolverType

from .fields import ThinktankField


class ResolverConfigSerializer(Serializer):
    type = ChoiceField(choices=ResolverType.choices)

    def get_serializer(self, type, *args, **kwargs):
        serializer_type = ResolverSerializers[type]
        return serializer_type(*args, **kwargs)

    def to_representation(self, instance):
        serializer = self.get_serializer(instance['type'], instance)

        return OrderedDict({**super().to_representation(instance), **serializer.to_representation(instance)})

    def to_internal_value(self, data):
        internal_data = super().to_internal_value(data)

        type = internal_data['type']

        serializer = self.get_serializer(type, data=data)

        return OrderedDict({**internal_data, **serializer.to_internal_value(data)})

    def validate(self, data):
        type = data['type']
        serializer = self.get_serializer(type, data=data)

        return {**super().validate(data), **serializer.validate(data)}


class PaginatorSerializer(Serializer):
    list_selector = CharField()
    button_selector = CharField()
    max_pages = IntegerField(min_value=1)


class ListResolverSerializer(Serializer):
    selector = CharField()
    paginator = PaginatorSerializer()
    resolvers = ResolverConfigSerializer(many=True)


class LinkResolverSerializer(Serializer):
    selector = CharField()
    resolvers = ResolverConfigSerializer(many=True)


class DataResolverSerializer(Serializer):
    key = ChoiceField(choices=DataResolverKey.choices)
    selector = CharField(required=True)


class AttributeResolverSerializer(DataResolverSerializer):
    attribute = CharField(required=True)


class StaticResolverSerializer(Serializer):
    key = ChoiceField(choices=DataResolverKey.choices)
    value = CharField()


class DocumentResolverSerializer(Serializer):
    selector = CharField()


ResolverSerializers = {
    ResolverType.LIST: ListResolverSerializer,
    ResolverType.LINK: LinkResolverSerializer,
    ResolverType.DATA: DataResolverSerializer,
    ResolverType.ATTRIBUTE: AttributeResolverSerializer,
    ResolverType.STATIC: StaticResolverSerializer,
    ResolverType.DOCUMENT: DocumentResolverSerializer,
}


class ScraperSerializer(ModelSerializer):
    REQUIRED_KEYS = ['title']

    thinktank = ThinktankField()
    data = ResolverConfigSerializer()

    class Meta:
        model = Scraper
        fields = ['id', 'type', 'thinktank', 'is_active', 'data', 'start_url', 'interval', 'last_run']

    def validate(self, attrs):
        super().validate(attrs)

        keys = self.get_keys(attrs)

        missing = set(self.REQUIRED_KEYS) - set(keys)

        if missing:
            raise ValidationError(
                detail=_('There must be a resolver for the following fields: %s') % ','.join(missing),
                code='missing-resolvers',
            )

        return attrs

    def get_keys(self, value, key=None):
        if key == 'key' and isinstance(value, str):
            return [value]

        keys = []

        if isinstance(value, dict):
            for k, v in value.items():
                keys += self.get_keys(v, key=k)

        elif isinstance(value, list):
            for v in value:
                keys += self.get_keys(v)

        return keys


class ScraperListSerializer(ModelSerializer):
    """
    Light serializer for nested scraper lists.
    """

    class Meta:
        model = Scraper
        read_only_fields = ['error_count', 'thinktank_id']
        fields = [
            'id',
            'thinktank_id',
            'type',
            'start_url',
            'last_run',
            'interval',
            'is_active',
            *read_only_fields,
        ]
