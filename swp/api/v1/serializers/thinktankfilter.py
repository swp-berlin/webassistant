from rest_framework import serializers

from swp.api.v1.serializers.publicationfilter import PublicationFilterSerializer
from swp.models import Publication, ThinktankFilter


class ThinktankFilterSerializer(serializers.ModelSerializer):
    filters = PublicationFilterSerializer(source='publication_filters', many=True)
    publication_count = serializers.SerializerMethodField('get_filter_count')

    class Meta:
        model = ThinktankFilter
        fields = ['id', 'name', 'monitor', 'thinktank', 'filters', 'publication_count']

    def get_filter_count(self, thinktank_filter: ThinktankFilter):
        # FIXME this executes one query for each thinktank filter
        return Publication.objects.filter(thinktank_filter.as_query).count()
