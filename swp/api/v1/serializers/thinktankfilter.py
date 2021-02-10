from django.db import transaction
from rest_framework import serializers

from swp.api.v1.serializers.fields import MonitorField
from swp.api.v1.serializers.publicationfilter import PublicationFilterSerializer
from swp.models import Publication, PublicationFilter, ThinktankFilter


class ThinktankFilterSerializer(serializers.ModelSerializer):
    filters = PublicationFilterSerializer(source='publication_filters', many=True)
    publication_count = serializers.SerializerMethodField('get_filter_count')
    monitor = MonitorField(read_only=True)

    class Meta:
        model = ThinktankFilter
        fields = ['id', 'name', 'monitor', 'thinktank', 'filters', 'publication_count']

    def get_filter_count(self, thinktank_filter: ThinktankFilter):
        # FIXME this executes one query for each thinktank filter
        return Publication.objects.active().filter(thinktank_filter.as_query).count()

    @transaction.atomic
    def create(self, validated_data):
        publication_filters = validated_data.pop('publication_filters')

        thinktank_filter = super().create(validated_data)
        self.create_publication_filters(thinktank_filter, publication_filters)

        return thinktank_filter

    def create_publication_filters(self, thinktank_filter, publication_filters):
        PublicationFilter.objects.bulk_create([
            PublicationFilter(thinktank_filter=thinktank_filter, *filter) for filter in publication_filters
        ])

    @transaction.atomic
    def update(self, instance, validated_data):
        publication_filters = validated_data.pop('publication_filters')

        thinktank_filter = super().update(instance, validated_data)
        self.update_publication_filters(instance, publication_filters)

        return thinktank_filter

    def update_publication_filters(self, thinktank_filter, publication_filters):
        ids = [filter.get('id') for filter in publication_filters if filter.get('id')]

        PublicationFilter.objects.filter(thinktank_filter=thinktank_filter).exclude(pk__in=ids).delete()

        for filter in publication_filters:
            id = filter.get('id')

            if id:
                PublicationFilter.objects.filter(thinktank_filter=thinktank_filter, pk=id).update(**filter)
            else:
                PublicationFilter.objects.create(thinktank_filter=thinktank_filter, **filter)
