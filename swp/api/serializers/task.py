from contextlib import suppress

from celery.result import AsyncResult
from celery.states import *

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.serializers import Serializer

STATES = [
    PENDING,
    RECEIVED,
    STARTED,
    SUCCESS,
    FAILURE,
    RETRY,
    REVOKED,
]


class BaseAsyncTaskResultSerializer(Serializer):
    id = serializers.CharField(label=_('ID'), read_only=True)
    status = serializers.ChoiceField(label=_('status'), choices=STATES, read_only=True)
    result = serializers.SerializerMethodField(label=_('result'), read_only=True)

    @staticmethod
    def get_result(instance: AsyncResult):
        with suppress(instance.TimeoutError):
            return instance.get(timeout=0.1, propagate=False)
