import uuid

from unittest.mock import patch

from celery.result import AsyncResult
from celery.states import PENDING

from rest_framework.test import APITestCase

from swp.models import Scraper, Interval
from swp.tasks import preview_scraper
from swp.utils.testing import create_scraper, create_thinktank, create_user, login, request

from .serializers import BaseScraperSerializer


class FakeResult:
    id = uuid.uuid4()
    status = PENDING
    TimeoutError = AsyncResult.TimeoutError

    @classmethod
    def get(cls, **kwargs):
        raise cls.TimeoutError(f'{kwargs}')


class ScraperStartURLTestSerializer(BaseScraperSerializer):

    class Meta:
        model = Scraper
        fields = [
            'thinktank',
            'start_url',
        ]


class ScraperTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = create_user('tester', is_superuser=True)
        cls.thinktank = thinktank = create_thinktank('Test')
        cls.scraper = create_scraper(thinktank)

    def setUp(self):
        login(self)

    def test_active_scraper_not_editable(self):
        self.scraper.activate(self.user)

        request(self, '1:scraper-detail', args=[self.scraper.id], status_code=400,
                method='PATCH', data={'interval': Interval.WEEKLY.value})

    def test_inactive_scraper_editable(self):
        self.scraper.deactivate(self.user)

        request(self, '1:scraper-detail', args=[self.scraper.id],
                method='PATCH', data={'interval': Interval.WEEKLY.value})

    def test_scraper_preview(self):
        with patch.object(preview_scraper, 'delay', return_value=FakeResult):
            request(self, '1:scraper-preview', args=[self.scraper.id], method='PATCH', data={})

    def test_scraper_preview_status(self):
        with patch.object(preview_scraper, 'AsyncResult', return_value=FakeResult):
            request(self, '1:scraper-preview-status', args=[f'{FakeResult.id}'])

    def test_scraper_start_url_validation(self):
        data = {
            'thinktank': self.thinktank.id,
            'start_url': self.thinktank.url,
        }

        serializer = ScraperStartURLTestSerializer(data=data)
        result = serializer.is_valid(raise_exception=False)

        self.assertTrue(result)

        data.pop('thinktank')

        serializer = ScraperStartURLTestSerializer(data=data, partial=True)
        result = serializer.is_valid(raise_exception=False)

        self.assertTrue(result)
