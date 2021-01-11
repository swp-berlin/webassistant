from rest_framework.serializers import ModelSerializer

from swp.models import Thinktank


class ThinktankSerializer(ModelSerializer):

    class Meta:
        model = Thinktank
        read_only_fields = [
            'is_active',
            'last_run',
            'created',
            'publication_count',
            'scraper_count',
            'last_error_count',
        ]
        fields = [
            'id',
            'name',
            'description',
            'url',
            'unique_field',
            *read_only_fields,
        ]
