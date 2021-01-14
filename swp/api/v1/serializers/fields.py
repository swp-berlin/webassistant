from rest_framework import serializers
from swp.models import Thinktank


class ThinktankField(serializers.ModelSerializer):

    class Meta:
        model = Thinktank
        fields = ['id', 'name']
        read_only_fields = ['id']
