from django.utils import translation

from swp.management.scheme import GenerateSchemeCommand
from swp.scraper.types import ScraperTypeChoices


class Command(GenerateSchemeCommand):
    filename = 'scraperTypes.json'

    @translation.override(None)
    def get_data(self, **options):
        return [
            {
                'value': choice.value,
                'label': f'{choice.label}',
                'defaults': choice.defaults,
            }
            for choice in ScraperTypeChoices
        ]
