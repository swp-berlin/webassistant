from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from swp.api.v1.serializers.fields import ThinktankField
from swp.models import Publication


class PublicationSerializer(ModelSerializer):

    thinktank = ThinktankField()

    class Meta:
        model = Publication
        read_only_fields = [
            'thinktank',
            'created',
        ]
        fields = [
            'id',
            'thinktank',
            'title',
            'subtitle',
            'ris_type',
            'authors',
            'abstract',
            'publication_date',
            'last_access',
            'url',
            'pdf_url',
            'pdf_pages',
            'tags',
            *read_only_fields,
        ]
