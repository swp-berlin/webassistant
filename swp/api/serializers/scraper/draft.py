from rest_framework.fields import CharField, ChoiceField, IntegerField
from rest_framework.serializers import Serializer

from swp.models import Scraper
from swp.models.choices import PaginatorType, ResolverType

from .base import BaseScraperSerializer, ResolverConfigSerializer
from .resolver import ResolverTypeField
from ..fields import CSSSelectorField


class ResolverConfigDraftSerializer(ResolverConfigSerializer):
    pass


class PaginatorDraftSerializer(Serializer):
    type = ChoiceField(choices=PaginatorType.choices)
    list_selector = CSSSelectorField(allow_blank=True)
    button_selector = CSSSelectorField(allow_blank=True)
    max_pages = IntegerField(min_value=1)


@ResolverConfigDraftSerializer.register(ResolverType.LIST)
class ListResolverDraftSerializer(Serializer):
    selector = CSSSelectorField(allow_blank=True)
    cookie_banner_selector = CSSSelectorField(allow_blank=True, default='')
    paginator = PaginatorDraftSerializer()
    resolvers = ResolverConfigDraftSerializer(many=True)


@ResolverConfigDraftSerializer.register(ResolverType.LINK)
class LinkResolverDraftSerializer(Serializer):
    selector = CSSSelectorField(allow_blank=True)
    resolvers = ResolverConfigDraftSerializer(many=True)


@ResolverConfigDraftSerializer.register(ResolverType.DATA)
class DataResolverDraftSerializer(Serializer):
    selector = CSSSelectorField(allow_blank=True)


@ResolverConfigDraftSerializer.register(ResolverType.ATTRIBUTE)
class AttributeResolverDraftSerializer(DataResolverDraftSerializer):
    attribute = CharField(allow_blank=True)


@ResolverConfigDraftSerializer.register(ResolverType.STATIC)
class StaticResolverDraftSerializer(Serializer):
    value = CharField(allow_blank=True)


@ResolverConfigDraftSerializer.register(ResolverType.DOCUMENT)
class DocumentResolverDraftSerializer(Serializer):
    key = CharField(default='pdf_url')
    selector = CSSSelectorField(allow_blank=True)


@ResolverConfigDraftSerializer.register(ResolverType.EMBEDDINGS)
class EmbeddingsResolverDraftSerializer(Serializer):
    key = CharField(default='text_content')
    selector = CSSSelectorField(allow_blank=True)


@ResolverConfigDraftSerializer.register(*ResolverTypeField)
class FieldResolverDraftSerializer(Serializer):
    resolver = ResolverConfigDraftSerializer()


class ScraperDraftSerializer(BaseScraperSerializer):
    data = ResolverConfigDraftSerializer()

    class Meta:
        model = Scraper
        fields = ['start_url', 'type', 'interval', 'data', 'categories']
