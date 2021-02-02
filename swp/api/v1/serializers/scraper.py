from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, ChoiceField, IntegerField
from rest_framework.serializers import ModelSerializer, Serializer

from cosmogo.utils.text import enumeration

from swp.models import Scraper
from swp.models.choices import DataResolverKey, ResolverType

from .fields import ThinktankField, CSSSelectorField


class ResolverConfigSerializer(Serializer):
    type = ChoiceField(choices=ResolverType.choices)

    def get_serializer(self, type, *args, **kwargs):
        serializer_type = ResolverSerializers[type]
        return serializer_type(*args, **kwargs)

    def to_representation(self, instance):
        serializer = self.get_serializer(instance['type'], instance)

        return {**super().to_representation(instance), **serializer.to_representation(instance)}

    def to_internal_value(self, data):
        internal_data = super().to_internal_value(data)

        type = internal_data['type']

        serializer = self.get_serializer(type, data=data)

        return {**internal_data, **serializer.to_internal_value(data)}

    def validate(self, data):
        type = data['type']
        serializer = self.get_serializer(type, data=data)

        return {**super().validate(data), **serializer.validate(data)}


class PaginatorSerializer(Serializer):
    type = CharField(default='Page')
    list_selector = CSSSelectorField()
    button_selector = CSSSelectorField(allow_blank=True)
    max_pages = IntegerField(min_value=1)


class ListResolverSerializer(Serializer):
    selector = CSSSelectorField()
    paginator = PaginatorSerializer()
    resolvers = ResolverConfigSerializer(many=True)


class LinkResolverSerializer(Serializer):
    selector = CSSSelectorField()
    resolvers = ResolverConfigSerializer(many=True)


class DataResolverSerializer(Serializer):
    key = ChoiceField(choices=DataResolverKey.choices)
    selector = CSSSelectorField(required=True)


class AttributeResolverSerializer(DataResolverSerializer):
    attribute = CharField(required=True)


class StaticResolverSerializer(Serializer):
    key = ChoiceField(choices=DataResolverKey.choices)
    value = CharField()


class DocumentResolverSerializer(Serializer):
    key = CharField(default='pdf_url')
    selector = CSSSelectorField()


class TagResolverSerializer(Serializer):
    resolver = ResolverConfigSerializer()


class TagDataResolverSerializer(Serializer):
    selector = CSSSelectorField(required=True)


class TagAttributeResolverSerializer(TagDataResolverSerializer):
    attribute = CharField(required=True)


class TagStaticResolverSerializer(Serializer):
    key = ChoiceField(choices=DataResolverKey.choices)
    value = CharField()


ResolverSerializers = {
    ResolverType.LIST: ListResolverSerializer,
    ResolverType.LINK: LinkResolverSerializer,
    ResolverType.DATA: DataResolverSerializer,
    ResolverType.ATTRIBUTE: AttributeResolverSerializer,
    ResolverType.STATIC: StaticResolverSerializer,
    ResolverType.DOCUMENT: DocumentResolverSerializer,
    ResolverType.TAG: TagResolverSerializer,
    ResolverType.TAG_DATA: TagDataResolverSerializer,
    ResolverType.TAG_ATTRIBUTE: TagAttributeResolverSerializer,
    ResolverType.TAG_STATIC: TagStaticResolverSerializer,
}


class ScraperSerializer(ModelSerializer):
    REQUIRED_KEYS = ['title']

    thinktank = ThinktankField(read_only=True)
    data = ResolverConfigSerializer(required=True)

    class Meta:
        model = Scraper
        read_only_fields = [
            'name',
            'last_run',
        ]
        fields = ['id', 'name', 'type', 'thinktank', 'is_active', 'data', 'start_url', 'interval', 'last_run']

    def validate_data(self, data):
        keys = self.get_keys(data)

        missing = {*self.REQUIRED_KEYS} - {*keys}

        if missing:
            message = _('There must be a resolver for the following fields: %(fields)s')
            labels = dict(DataResolverKey.choices)
            missing_labels = [labels[field] for field in missing]
            raise ValidationError(detail=message % {'fields': enumeration(missing_labels)}, code='missing-resolvers')

        return data

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
