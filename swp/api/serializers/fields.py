from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from swp.models import Monitor, Publication, Thinktank

from .validators import css_selector


class ThinktankField(serializers.ModelSerializer):

    class Meta:
        model = Thinktank
        fields = ['id', 'name']
        read_only_fields = ['id']


class MonitorField(serializers.ModelSerializer):
    class Meta:
        model = Monitor
        fields = ['id', 'name']
        read_only_fields = ['id']


class PublicationField(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = ['id', 'url', 'title']
        read_only_fields = ['id']


class CSSSelectorField(serializers.CharField):
    default_validators = [css_selector]


class RecipientsField(serializers.ListField):
    child = serializers.EmailField()

    def run_child_validation(self, data):
        result = []
        errors = []

        for idx, item in enumerate(data):
            try:
                result.append(self.child.run_validation(item))
            except ValidationError as e:
                errors.extend(e.detail)

        if not errors:
            return result

        raise ValidationError(errors)
