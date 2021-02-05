from rest_framework import serializers

from swp.api.v1.serializers.thinktankfilter import ThinktankFilterSerializer
from swp.models import Monitor, Publication, ThinktankFilter


class MonitorSerializer(serializers.ModelSerializer):
    filters = ThinktankFilterSerializer(source='thinktank_filters', many=True)
    publication_count = serializers.SerializerMethodField('get_filter_count')

    class Meta:
        model = ThinktankFilter
        fields = ['id', 'filters', 'publication_count']

    def get_filter_count(self, monitor: Monitor):
        # FIXME this executes one query for each monitor
        return Publication.objects.filter(monitor.as_query).count()
