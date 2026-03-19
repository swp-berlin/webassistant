from typing import Optional

from django.utils.translation import gettext_lazy as _

from celery.result import AsyncResult

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from swp.api.serializers.task import BaseAsyncTaskResultSerializer
from swp.api.v1.serializers import ActivatableSerializer
from swp.models import Scraper
from swp.tasks import preview_scraper, run_scraper
from swp.tasks.scraper import PreviewResult

from .fields import ResolverConfigSerializer


class BaseScraperSerializer(ModelSerializer):

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


class ScraperSerializer(ActivatableSerializer, BaseScraperSerializer):
    data = ResolverConfigSerializer(label=_('data'))

    class Meta:
        model = Scraper
        fields = serializers.ALL_FIELDS


class ScraperPreviewSerializer(BaseScraperSerializer, BaseAsyncTaskResultSerializer):
    data = ResolverConfigSerializer(label=_('data'), write_only=True)

    class Meta:
        model = Scraper
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
        return BaseAsyncTaskResultSerializer.get_result(instance)


class ScraperRunSerializer(BaseAsyncTaskResultSerializer):
    force_update = serializers.BooleanField(label=_('force update'), write_only=True, required=False)

    def update(self, instance: Scraper, validated_data):
        force_update = validated_data.get('force_update', False)

        instance.update(modified=False, is_running=True)

        return run_scraper.delay(instance.id, force=True, force_update=force_update)

    @staticmethod
    def get_result(instance: AsyncResult) -> Optional[int]:
        return BaseAsyncTaskResultSerializer.get_result(instance)
