from rest_framework.serializers import SerializerMetaclass, Serializer

from swp.models.choices import ResolverType

ResolverTypeField = [
    ResolverType.TITLE,
    ResolverType.SUBTITLE,
    ResolverType.ABSTRACT,
    ResolverType.PUBLICATION_DATE,
    ResolverType.URL,
    ResolverType.AUTHORS,
    ResolverType.DOI,
    ResolverType.ISBN,
    ResolverType.TAGS,
]


class ResolverConfigSerializerMeta(SerializerMetaclass):

    def __new__(cls, name, bases, attrs):
        attrs['serializers'] = {}

        return super().__new__(cls, name, bases, attrs)


class BaseResolverConfigSerializer(Serializer, metaclass=ResolverConfigSerializerMeta):
    serializers: dict

    @classmethod
    def register(cls, *resolver_types: ResolverType):
        def inner(serializer_class):
            for resolver_type in resolver_types:
                cls.serializers[resolver_type] = serializer_class

            return serializer_class

        return inner

    @classmethod
    def get_serializer(cls, resolver_type: ResolverType, *args, **kwargs):
        return cls.serializers[resolver_type](*args, **kwargs)
