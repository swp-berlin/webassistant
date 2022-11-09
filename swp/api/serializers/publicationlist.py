from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from swp.models import PublicationList

from .publication import PublicationSerializer


class PublicationListSerializer(ModelSerializer):
    entry_count = serializers.IntegerField(read_only=True)
    last_updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = PublicationList
        fields = [
            'id',
            'name',
            'entry_count',
            'last_updated',
        ]


class PublicationListDetailSerializer(PublicationListSerializer):
    publications = PublicationSerializer(many=True)

    class Meta(PublicationListSerializer.Meta):
        fields = [
            *PublicationListSerializer.Meta.fields,
            'publications',
        ]
