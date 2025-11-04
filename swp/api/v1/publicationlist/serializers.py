from rest_framework.serializers import ModelSerializer

from swp.models import PublicationList, PublicationListEntry


class PublicationListEntrySerializer(ModelSerializer):

    class Meta:
        model = PublicationListEntry
        exclude = ['publication_list']


class PublicationListSerializer(ModelSerializer):
    entries = PublicationListEntrySerializer(many=True)

    class Meta:
        model = PublicationList
        exclude = ['user', 'publications']
