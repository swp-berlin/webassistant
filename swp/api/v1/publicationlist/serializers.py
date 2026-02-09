from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

from swp.api.v1.publication import PublicationSerializer
from swp.models import Publication, PublicationList, PublicationListEntry


class PublicationListEntrySerializer(ModelSerializer):

    class Meta:
        model = PublicationListEntry
        exclude = ['publication_list']


class PublicationListEntryWithObjectSerializer(PublicationListEntrySerializer):
    publication = PublicationSerializer(read_only=True)


class PublicationListSerializer(ModelSerializer):
    entries = PublicationListEntrySerializer(label=_('entries'), many=True, read_only=True)
    last_updated = serializers.DateTimeField(label=_('last updated'), read_only=True)

    class Meta:
        model = PublicationList
        exclude = ['user', 'publications']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if user := self.context['request'].user:
            self.add_unique_name_validator(user)

    def add_unique_name_validator(self, user):
        field = self.fields['name']
        queryset = PublicationList.objects.filter(user=user)
        message = _('You already have a publication list with this name.')
        validator = UniqueValidator(queryset, message)
        field.validators = [*field.validators, validator]


class PublicationListWithObjectsSerializer(PublicationListSerializer):
    entries = PublicationListEntryWithObjectSerializer(label=_('entries'), many=True, read_only=True)


class PublicationListUpdateSerializer(PublicationListSerializer):
    publication = serializers.PrimaryKeyRelatedField(
        label=_('publication'),
        queryset=Publication.objects,
        write_only=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in set(self.fields) - {'publication'}:
            self.fields[field].read_only = True

    def entry_exists(self, publication: Publication):
        return PublicationListEntry.objects.filter(publication_list=self.instance, publication=publication).exists()

    def fail_entry(self, key: str, publication: Publication):
        return self.fail(key, publication=publication, list=self.instance)


class PublicationListAddSerializer(PublicationListUpdateSerializer):
    default_error_messages = {
        'already-an-entry': _('Publication „{publication}“ is already an entry of list „{list}“.'),
    }

    def validate_publication(self, publication: Publication):
        if self.entry_exists(publication):
            return self.fail_entry('already-an-entry', publication)

        return publication

    def update(self, instance: PublicationList, validated_data):
        PublicationListEntry.objects.create(
            publication_list=instance,
            publication=validated_data['publication'],
            created=self.context['request'].now,
        )

        return instance


class PublicationListRemoveSerializer(PublicationListUpdateSerializer):
    default_error_messages = {
        'not-an-entry': _('Publication „{publication}“ is not an entry of list „{list}“.'),
    }

    def validate_publication(self, publication: Publication):
        if self.entry_exists(publication):
            return publication

        return self.fail_entry('not-an-entry', publication)

    def update(self, instance: PublicationList, validated_data):
        PublicationListEntry.objects.filter(
            publication_list=instance,
            publication=validated_data['publication'],
        ).delete()

        instance.update(modified=True)

        return instance
