from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from swp.models import Monitor, Pool

from .fields import RecipientsField
from .pool import PoolSerializer


class PoolField(PrimaryKeyRelatedField):

    def get_queryset(self):
        return Pool.objects.annotate_can_manage(self.context.get('request').user)

    def use_pk_only_optimization(self):
        return False

    def to_representation(self, value):
        return PoolSerializer(value).data


class BaseMonitorSerializer(ModelSerializer):
    pool = PoolField()

    class Meta:
        model = Monitor
        fields = [
            'id',
            'name',
            'pool',
            'is_active',
        ]


class MonitorSerializer(BaseMonitorSerializer):
    recipient_count = serializers.IntegerField(read_only=True)
    publication_count = serializers.IntegerField(read_only=True)
    new_publication_count = serializers.IntegerField(read_only=True)

    class Meta(BaseMonitorSerializer.Meta):
        fields = [
            *BaseMonitorSerializer.Meta.fields,
            'last_sent',
            'recipient_count',
            'publication_count',
            'new_publication_count',
        ]


class MonitorDetailSerializer(MonitorSerializer):

    class Meta(MonitorSerializer.Meta):
        fields = [
            *MonitorSerializer.Meta.fields,
            'description',
            'query',
            'interval',
            'last_publication_count_update',
        ]


class MonitorTransferredSerializer(ModelSerializer):
    transferred_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Monitor
        fields = [
            'transferred_count',
        ]


class MonitorEditSerializer(BaseMonitorSerializer):
    recipients = RecipientsField()

    def __init__(self, instance=None, **kwargs):
        super().__init__(instance, **kwargs)

        if instance is None:
            self.fields.pop('query')

    class Meta(BaseMonitorSerializer.Meta):
        fields = [
            *BaseMonitorSerializer.Meta.fields,
            'description',
            'query',
            'interval',
            'recipients',
            'zotero_keys',
        ]

    def validate(self, attrs):
        self.validate_active_monitor_has_query(attrs)

        return attrs

    def validate_active_monitor_has_query(self, attrs):
        if instance := self.instance:
            query = attrs.get('query', instance.query)
            is_active = attrs.get('is_active', instance.is_active)
        else:
            query = attrs.get('query')
            is_active = attrs.get('is_active')

        instance = Monitor(query=query, is_active=is_active)

        return Monitor.clean(instance)
