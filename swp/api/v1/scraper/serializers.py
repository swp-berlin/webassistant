from contextlib import suppress
from typing import Optional

from django.utils.translation import gettext_lazy as _

from celery.exceptions import TimeoutError
from celery.result import AsyncResult
from celery.states import *

from rest_framework import serializers

from swp.api.v1.serializers import ActivatableSerializer
from swp.models import Scraper
from swp.tasks import preview_scraper
from swp.tasks.scraper import PreviewResult

STATES = [
    PENDING,
    RECEIVED,
    STARTED,
    SUCCESS,
    FAILURE,
    RETRY,
    REVOKED,
]


class ScraperSerializer(ActivatableSerializer):

    class Meta:
        model = Scraper
        fields = serializers.ALL_FIELDS

    def validate(self, attrs):
        self.validate_start_url_domain(attrs)

        return attrs

    def validate_start_url_domain(self, attrs):
        if instance := self.instance:
            thinktank = attrs.get('thinktank', instance.thinktank)
            start_url = attrs.get('start_url', instance.start_url)
        else:
            thinktank = attrs.get('thinktank')
            start_url = attrs.get('start_url')

        if None in {thinktank, start_url}:
            return None

        Scraper.validate_start_url(start_url, thinktank.domain)


class ScraperPreviewSerializer(ScraperSerializer):
    id = serializers.CharField(label=_('ID'), read_only=True)
    status = serializers.ChoiceField(label=_('status'), choices=STATES, read_only=True)
    result = serializers.SerializerMethodField(label=_('result'), read_only=True)

    class Meta(ScraperSerializer.Meta):
        fields = [
            'id',
            'status',
            'result',
            'start_url',
            'data',
        ]
        extra_kwargs = {
            'start_url': {
                'write_only': True,
            },
            'data': {
                'write_only': True,
            },
        }

    def update(self, instance: Scraper, validated_data):
        start_url = validated_data.get('start_url', instance.start_url)
        data = validated_data.get('data', instance.data)

        return preview_scraper.delay(start_url, data)

    @staticmethod
    def get_result(instance: AsyncResult) -> Optional[PreviewResult]:
        with suppress(TimeoutError):
            return instance.get(timeout=0.1, propagate=False)
