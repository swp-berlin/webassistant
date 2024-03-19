from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, ChoiceField, IntegerField
from rest_framework.serializers import ModelSerializer, Serializer

from swp.models import Scraper, Thinktank
from swp.models.choices import PaginatorType, ResolverType
from swp.utils.text import enumeration

from .resolver import BaseResolverConfigSerializer, ResolverTypeField
from ..fields import ThinktankField, CSSSelectorField
from ..scrapererror import ScraperErrorSerializer


class ResolverConfigSerializer(BaseResolverConfigSerializer):
    type = ChoiceField(choices=ResolverType.choices)

    def to_representation(self, instance):
        serializer = self.get_serializer(instance['type'], instance)

        return {**super().to_representation(instance), **serializer.to_representation(instance)}

    def to_internal_value(self, data):
        internal_data = super().to_internal_value(data)
        serializer = self.get_serializer(internal_data['type'], data=data)

        return {**internal_data, **serializer.to_internal_value(data)}

    def validate(self, data):
        serializer = self.get_serializer(data['type'], data=data)

        return {**super().validate(data), **serializer.validate(data)}


class PaginatorSerializer(Serializer):
    type = ChoiceField(choices=PaginatorType.choices)
    list_selector = CSSSelectorField()
    button_selector = CSSSelectorField(allow_blank=True)
    max_pages = IntegerField(min_value=1)


@ResolverConfigSerializer.register(ResolverType.LIST)
class ListResolverSerializer(Serializer):
    selector = CSSSelectorField()
    cookie_banner_selector = CSSSelectorField(allow_blank=True, default='')
    paginator = PaginatorSerializer()
    resolvers = ResolverConfigSerializer(many=True)


@ResolverConfigSerializer.register(ResolverType.LINK)
class LinkResolverSerializer(Serializer):
    selector = CSSSelectorField()
    resolvers = ResolverConfigSerializer(many=True)


@ResolverConfigSerializer.register(ResolverType.DATA)
class DataResolverSerializer(Serializer):
    selector = CSSSelectorField(required=True)


@ResolverConfigSerializer.register(ResolverType.ATTRIBUTE)
class AttributeResolverSerializer(DataResolverSerializer):
    attribute = CharField(required=True)


@ResolverConfigSerializer.register(ResolverType.STATIC)
class StaticResolverSerializer(Serializer):
    value = CharField()


@ResolverConfigSerializer.register(ResolverType.DOCUMENT)
class DocumentResolverSerializer(Serializer):
    key = CharField(default='pdf_url')
    selector = CSSSelectorField()


@ResolverConfigSerializer.register(*ResolverTypeField)
class FieldResolverSerializer(Serializer):
    resolver = ResolverConfigSerializer()


class BaseScraperSerializer(ModelSerializer):

    def __init__(self, instance=None, *args, thinktank: Thinktank = None, **kwargs):
        self.thinktank = thinktank or instance.thinktank
        ModelSerializer.__init__(self, instance, *args, **kwargs)

    def validate(self, attrs):
        self.validate_start_url_domain(attrs)

        return attrs

    def validate_start_url_domain(self, attrs):
        if attrs.get('is_active', None) is False:
            return None

        if instance := self.instance:
            start_url = attrs.get('start_url', instance.start_url)
        else:
            start_url = attrs.get('start_url')

        if start_url is None:
            return None

        Scraper.validate_start_url(start_url, self.thinktank.domain)


class ScraperSerializer(BaseScraperSerializer):
    REQUIRED_RESOLVERS = {ResolverType.TITLE.value}

    thinktank = ThinktankField(read_only=True)
    data = ResolverConfigSerializer()
    errors = ScraperErrorSerializer(many=True, read_only=True)

    class Meta:
        model = Scraper
        read_only_fields = [
            'name',
            'last_run',
        ]
        fields = [
            'id',
            'name',
            'type',
            'thinktank',
            'data',
            'start_url',
            'interval',
            'is_active',
            'errors',
        ]

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if not self.partial or attrs.get('data'):
            self.check_missing_fields(attrs)

        return attrs

    def check_missing_fields(self, data):
        resolver_types = self.get_resolver_types(data)

        missing = self.REQUIRED_RESOLVERS - resolver_types

        if missing:
            message = _('There must be a resolver for the following fields: %(fields)s')
            labels = dict(ResolverType.choices)
            missing_labels = [labels[field] for field in missing]
            raise ValidationError(detail=message % {'fields': enumeration(missing_labels)}, code='missing-resolvers')

        return data

    def get_resolver_types(self, value, key=None):
        if key == 'type' and isinstance(value, str):
            return {value}

        keys = set()

        if isinstance(value, dict):
            for k, v in value.items():
                keys.update(self.get_resolver_types(v, key=k))

        elif isinstance(value, list):
            for v in value:
                keys.update(self.get_resolver_types(v))

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
