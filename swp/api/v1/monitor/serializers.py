from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from swp.models import Monitor


class MonitorSerializer(ModelSerializer):

    class Meta:
        model = Monitor
        fields = serializers.ALL_FIELDS
