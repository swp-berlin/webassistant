from rest_framework import serializers
from swp.models import Monitor, Thinktank
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


class CSSSelectorField(serializers.CharField):
    default_validators = [css_selector]
