from django.test import SimpleTestCase

from swp.scraper.types import ScraperType
from swp.utils.snippets import get_template


class ScraperTypeTestCase(SimpleTestCase):

    def test_descriptions_exists(self):
        # raises TemplateDoesNotExist when a description is missing
        for identifier in ScraperType.values:
            get_template(identifier=f'scraper-type/{identifier}')
