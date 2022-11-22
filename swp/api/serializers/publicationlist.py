from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from swp.models import PublicationList

from .publication import PublicationSerializer


class PublicationListSerializer(ModelSerializer):
    entry_count = serializers.IntegerField(read_only=True)
    last_updated = serializers.DateTimeField(read_only=True)
    publication_list = serializers.ListField(child=serializers.IntegerField(), read_only=True)

    class Meta:
        model = PublicationList
        fields = [
            'id',
            'name',
            'entry_count',
            'last_updated',
            'publication_list',
        ]

    def validate_name(self, value):
        request = self.context.get('request')

        if request.user.publication_lists.filter(name=value).exists():
            raise ValidationError(_('A publication list with this name already exists.'), code='duplicate')

        return value


class PublicationListDetailSerializer(PublicationListSerializer):
    publications = PublicationSerializer(many=True)

    class Meta(PublicationListSerializer.Meta):
        fields = [
            *PublicationListSerializer.Meta.fields,
            'publications',
        ]
