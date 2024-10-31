from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from swp.models import Category


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
        ]


class CategoryChoiceSerializer(serializers.Serializer):
    value = serializers.IntegerField(source='id')
    label = serializers.CharField(source='name')
