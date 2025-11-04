from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from swp.models import Thinktank


class ThinktankSerializer(ModelSerializer):

    class Meta:
        model = Thinktank
        fields = serializers.ALL_FIELDS
