from rest_framework import serializers

from swp.api.v1.serializers import ActivatableSerializer
from swp.models import Monitor


class MonitorSerializer(ActivatableSerializer):

    class Meta:
        model = Monitor
        fields = serializers.ALL_FIELDS

    def validate(self, attrs):
        self.validate_active_monitor_has_query(attrs)

        return attrs

    def validate_active_monitor_has_query(self, attrs):
        instance = self.instance

        if instance is None:
            return None

        instance = Monitor(
            query=attrs.get('query', instance.query),
            is_active=self.activate or instance.is_active,
        )

        return Monitor.clean(instance)
