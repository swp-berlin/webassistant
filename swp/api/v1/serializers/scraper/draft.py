from rest_framework.fields import CharField, ChoiceField, IntegerField
from rest_framework.serializers import ModelSerializer, Serializer

from swp.models import Scraper
from swp.models.choices import PaginatorType, ResolverType
from swp.api.v1.serializers.scraper import base
from ..fields import CSSSelectorField


class ResolverConfigDraftSerializer(base.ResolverConfigSerializer):
    def get_serializer(self, type, *args, **kwargs):
        serializer_type = ResolverDraftSerializers[type]
        return serializer_type(*args, **kwargs)


class PaginatorDraftSerializer(Serializer):
    type = ChoiceField(choices=PaginatorType.choices)
    list_selector = CSSSelectorField(allow_blank=True)
    button_selector = CSSSelectorField(allow_blank=True)
    max_pages = IntegerField(min_value=1)


class ListResolverDraftSerializer(Serializer):
    selector = CSSSelectorField(allow_blank=True)
    cookie_banner_selector = CSSSelectorField(allow_blank=True, default='')
    paginator = PaginatorDraftSerializer()
    resolvers = ResolverConfigDraftSerializer(many=True)


class LinkResolverDraftSerializer(Serializer):
    selector = CSSSelectorField(allow_blank=True)
    resolvers = ResolverConfigDraftSerializer(many=True)


class DataResolverDraftSerializer(Serializer):
    selector = CSSSelectorField(allow_blank=True)


class AttributeResolverDraftSerializer(DataResolverDraftSerializer):
    attribute = CharField(allow_blank=True)


class StaticResolverDraftSerializer(Serializer):
    value = CharField(allow_blank=True)


class DocumentResolverDraftSerializer(Serializer):
    key = CharField(default='pdf_url')
    selector = CSSSelectorField(allow_blank=True)


class FieldResolverDraftSerializer(Serializer):
    resolver = ResolverConfigDraftSerializer()


ResolverDraftSerializers = {
    ResolverType.LIST: ListResolverDraftSerializer,
    ResolverType.LINK: LinkResolverDraftSerializer,
    ResolverType.DATA: DataResolverDraftSerializer,
    ResolverType.ATTRIBUTE: AttributeResolverDraftSerializer,
    ResolverType.STATIC: StaticResolverDraftSerializer,
    ResolverType.DOCUMENT: DocumentResolverDraftSerializer,

    ResolverType.TITLE: FieldResolverDraftSerializer,
    ResolverType.SUBTITLE: FieldResolverDraftSerializer,
    ResolverType.ABSTRACT: FieldResolverDraftSerializer,
    ResolverType.PUBLICATION_DATE: FieldResolverDraftSerializer,
    ResolverType.URL: FieldResolverDraftSerializer,
    ResolverType.AUTHORS: FieldResolverDraftSerializer,
    ResolverType.DOI: FieldResolverDraftSerializer,
    ResolverType.ISBN: FieldResolverDraftSerializer,
    ResolverType.TAGS: FieldResolverDraftSerializer,
}


class ScraperDraftSerializer(ModelSerializer):
    data = ResolverConfigDraftSerializer()

    class Meta:
        model = Scraper
        fields = ['start_url', 'type', 'interval', 'data']
