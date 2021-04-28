from __future__ import annotations
from typing import Any, Mapping, Optional, TYPE_CHECKING

from celery.states import READY_STATES
from django.utils.translation import gettext_lazy as _
from rest_framework.fields import CharField, SerializerMethodField
from rest_framework.serializers import Serializer

from swp.api.serializers.scraper.base import ResolverConfigSerializer
from swp.tasks.scraper import preview_scraper
if TYPE_CHECKING:
    from celery.result import AsyncResult


class PreviewSerializer(Serializer):
    id = CharField(read_only=True)
    status = CharField(read_only=True)
    result = SerializerMethodField(read_only=True)
    traceback = CharField(read_only=True)

    start_url = CharField(write_only=True)
    data = ResolverConfigSerializer(write_only=True)

    def save(self, **kwargs):
        self.instance = self.preview_scraper(**self.validated_data)

        return self.instance

    @staticmethod
    def preview_scraper(*, start_url, data, **kwargs):
        return preview_scraper.delay(start_url, data)

    def get_result(self, result: AsyncResult) -> Optional[Mapping[str, Any]]:
        if result.successful():
            return result.get(propagate=False)

        if self.instance.status in READY_STATES:
            return {'success': False, 'error': _('Internal Error')}

        return None
