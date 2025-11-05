from rest_framework import serializers

from swp.api.v1.serializers import ActivatableSerializer
from swp.models import Monitor


class MonitorSerializer(ActivatableSerializer):

    class Meta:
        model = Monitor
        fields = serializers.ALL_FIELDS
