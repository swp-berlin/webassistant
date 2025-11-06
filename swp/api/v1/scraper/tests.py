import uuid
from unittest.mock import patch

from celery.states import PENDING
from celery.exceptions import TimeoutError
from rest_framework.test import APITestCase

from swp.models import Interval
from swp.tasks import preview_scraper
from swp.utils.testing import create_scraper, create_thinktank, create_user, login, request


class FakeResult:
    id = uuid.uuid4()
    status = PENDING

    @classmethod
    def get(cls, **kwargs):
        raise TimeoutError(f'{kwargs}')


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
            request(self, '1:scraper-preview', args=[self.scraper.id], method='POST', data={})

    def test_scraper_preview_status(self):
        with patch.object(preview_scraper, 'AsyncResult', return_value=FakeResult):
            request(self, '1:scraper-preview-status', args=[f'{FakeResult.id}'])
