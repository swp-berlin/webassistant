from rest_framework.serializers import ModelSerializer

from swp.models import PublicationFilter


class PublicationFilterSerializer(ModelSerializer):

    class Meta:
        model = PublicationFilter
        fields = ['id', 'thinktank_filter', 'field', 'comparator', 'value']
        read_only_fields = ['thinktank_filter']
