from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from swp.models import Pool


class PoolSerializer(ModelSerializer):

    class Meta:
        model = Pool
        fields = serializers.ALL_FIELDS
