from rest_framework.serializers import ModelSerializer

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
            'tags',
            *read_only_fields,
        ]
