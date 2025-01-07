from django.test import SimpleTestCase

from swp.scraper.types import ScraperType
from swp.utils.snippets import get_template


class ScraperTypeTestCase(SimpleTestCase):

    def test_descriptions_exists(self):
        for identifier in ScraperType.values:
            with self.subTest(identifier=identifier):
                # raises TemplateDoesNotExist when a description is missing
                get_template(identifier=f'scraper-type/{identifier}')
