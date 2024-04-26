from asgiref.sync import sync_to_async

from django.test import TestCase
from django.utils.timezone import localtime

from swp.models import Scraper
from swp.utils.testing import create_scraper, create_thinktank


class ScraperTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.thinktank = create_thinktank('Scraper-Test')

    async def test_empty_author_no_error(self):
        scraper: Scraper = await sync_to_async(create_scraper)(self.thinktank)

        fields = {
            'url': f'{self.thinktank.url}/test',
            'title': 'Some Title',
            'authors': ['\n\t\n\t'],
            'publication_date': '\n\tApril 26, 2024\n\t',
            'abstract': '\n\t',
            'tags': ['tag'],
        }

        publication = await scraper.build_publication(fields, {}, thinktank=self.thinktank, now=localtime(None))

        self.assertIsNotNone(publication)
        self.assertFalse(await sync_to_async(scraper.errors.exists)())
