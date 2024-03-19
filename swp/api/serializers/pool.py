from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from swp.models import Pool


class PoolSerializer(ModelSerializer):
    can_manage = serializers.BooleanField(read_only=True)

    class Meta:
        model = Pool
        fields = [
            'id',
            'name',
            'can_manage',
        ]
