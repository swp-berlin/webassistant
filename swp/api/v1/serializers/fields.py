from rest_framework import serializers
from swp.models import Thinktank
from .validators import css_selector


class ThinktankField(serializers.ModelSerializer):

    class Meta:
        model = Thinktank
        fields = ['id', 'name']
        read_only_fields = ['id']


class CSSSelectorField(serializers.CharField):
    default_validators = [css_selector]
