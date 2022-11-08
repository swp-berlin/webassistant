from rest_framework import fields
from rest_framework.serializers import ModelSerializer, Serializer

from swp.models import Publication


class PublicationSerializer(ModelSerializer):

    class Meta:
        model = Publication
        read_only_fields = [
            'thinktank_id',
            'created',
        ]
        fields = [
            'id',
            'thinktank_id',
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
            'doi',
            'isbn',
            'tags',
            *read_only_fields,
        ]


class ResearchSerializer(PublicationSerializer):
    score = fields.FloatField(read_only=True)

    class Meta(PublicationSerializer.Meta):
        fields = [*PublicationSerializer.Meta.fields, 'score']


class TagSerializer(Serializer):
    tag = fields.CharField(source='key')
    count = fields.IntegerField(source='doc_count')
