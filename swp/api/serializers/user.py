from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from swp.models import User


class UserSerializer(ModelSerializer):
    name = serializers.CharField(source='get_full_name')
    groups = serializers.StringRelatedField(many=True)
    permissions = serializers.StringRelatedField(source='get_all_permissions', many=True)

    class Meta:
        model = User
        read_only_fields = [
            'is_superuser',
            'is_staff',
            'name',
            'groups',
            'permissions',
        ]
        fields = [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'is_active',
            *read_only_fields,
        ]
