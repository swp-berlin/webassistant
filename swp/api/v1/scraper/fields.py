from typing import Type, cast

from drf_spectacular.utils import extend_schema_field, PolymorphicProxySerializer

from rest_framework.serializers import ChoiceField, Serializer

from swp.api.serializers.scraper.base import ResolverConfigSerializer
from swp.api.serializers.scraper.resolver import ResolverTypeField
from swp.models.choices import ResolverType

SerializerType = Type[Serializer]

# Resolver types that do not have child resolvers.
ResolverTypeChildless = [
    ResolverType.DOCUMENT,
    ResolverType.EMBEDDINGS,
]

# Resolver types that could be child resolvers of field resolvers.
ResolverTypeFieldChild = [
    ResolverType.ATTRIBUTE,
    ResolverType.DATA,
    ResolverType.STATIC,
]

# Resolver types that could be children resolvers of list resolver.
ResolverTypeLinkChild = [
    *ResolverTypeField,
    *ResolverTypeChildless,
]

# Resolver types that could be children resolvers of link resolver.
ResolverTypeListChild = [
    ResolverType.LINK,
    *ResolverTypeLinkChild,
]


def build_serializer(resolver_type: ResolverType, serializer: SerializerType = None, name: str = None, **attrs):
    serializer = serializer or ResolverConfigSerializer.serializers[resolver_type]

    attrs['type'] = ChoiceField(choices=[resolver_type.choice], required=True)

    return cast(SerializerType, type(name or serializer.__name__, (serializer,), attrs))


def get_field_serializer_name(resolver_type: ResolverType):
    words = resolver_type.value.split('_')

    words.append('ResolverSerializer')

    return ''.join(words)


ChildlessResolverSerializers = [
    build_serializer(resolver_type)
    for resolver_type in ResolverTypeChildless
]

FieldChildResolverSerializers = [
    build_serializer(resolver_type)
    for resolver_type in ResolverTypeFieldChild
]

FieldChildResolverProxySerializer = PolymorphicProxySerializer(
    component_name='FieldChildResolver',
    resource_type_field_name='type',
    serializers=FieldChildResolverSerializers,
)

FieldResolverSerializers = [
    build_serializer(
        resolver_type=resolver_type,
        name=get_field_serializer_name(resolver_type),
        resolver=FieldChildResolverProxySerializer,
    ) for resolver_type in ResolverTypeField
]

LinkResolverProxySerializer = build_serializer(
    ResolverType.LINK,
    resolvers=PolymorphicProxySerializer(
        many=True,
        component_name='LinkChildResolvers',
        resource_type_field_name='type',
        serializers=[
            *FieldResolverSerializers,
            *ChildlessResolverSerializers,
        ],
    ),
)

ListResolverProxySerializer = build_serializer(
    ResolverType.LIST,
    resolvers=PolymorphicProxySerializer(
        many=True,
        component_name='ListChildResolvers',
        resource_type_field_name='type',
        serializers=[
            LinkResolverProxySerializer,
            *FieldResolverSerializers,
            *ChildlessResolverSerializers,
        ],
    ),
)

ResolverConfigSerializer = extend_schema_field(ListResolverProxySerializer)(ResolverConfigSerializer)
