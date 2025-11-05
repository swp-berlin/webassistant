from rest_framework import serializers

from swp.api.v1.serializers import ActivatableSerializer
from swp.models import Thinktank


class ThinktankSerializer(ActivatableSerializer):

    class Meta:
        model = Thinktank
        fields = serializers.ALL_FIELDS
