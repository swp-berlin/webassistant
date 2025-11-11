from typing import Dict

from rest_framework.fields import Field
from rest_framework.serializers import ModelSerializer

from swp.models import ActivatableModel


class ReadOnlyMixin:
    fields: Dict[str, Field]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.read_only = True


class ActivatableSerializer(ModelSerializer):

    def __init__(self, *args, activate: bool = None, **kwargs):
        self.activate = activate

        super().__init__(*args, **kwargs)

        self.fields['is_active'].read_only = True

        if activate is not None:
            for field in self.fields:
                self.fields[field].read_only = True

    def update(self, instance: ActivatableModel, validated_data):
        if self.activate is None:
            return super().update(instance, validated_data)

        user = self.context['request'].user

        if self.activate:
            instance.activate(user)
        else:
            instance.deactivate(user)

        return instance
