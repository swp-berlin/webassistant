from rest_framework import serializers

from swp.api.v1.serializers.thinktankfilter import ThinktankFilterSerializer
from swp.models import Monitor


class MonitorSerializer(serializers.ModelSerializer):
    recipient_count = serializers.IntegerField(read_only=True)
    publication_count = serializers.IntegerField(read_only=True)
    new_publication_count = serializers.IntegerField(read_only=True)

    filters = ThinktankFilterSerializer(source='thinktank_filters', many=True)

    class Meta:
        model = Monitor
        fields = ['id', 'name', 'recipient_count', 'publication_count', 'new_publication_count', 'filters']