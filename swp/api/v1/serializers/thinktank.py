from django.utils.translation import gettext_lazy as _

from rest_framework.fields import BooleanField
from rest_framework.serializers import ModelSerializer

from swp.models import Thinktank


class ThinktankSerializer(ModelSerializer):

    is_active = BooleanField(label=_('Active'), default=True, initial=True)

    class Meta:
        model = Thinktank
        read_only_fields = [
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
            'is_active',
            *read_only_fields,
        ]
