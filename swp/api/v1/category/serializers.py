from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from swp.models import Category


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = serializers.ALL_FIELDS
