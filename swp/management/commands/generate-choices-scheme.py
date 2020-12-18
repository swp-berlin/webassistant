from django.utils import translation

from swp.management.scheme import GenerateSchemeCommand
from swp.models.choices import Interval, ScraperType


class Command(GenerateSchemeCommand):
    PROPERTIES = [
        ('ScraperType', ScraperType.choices),
        ('interval', Interval.choices),
    ]

    filename = 'choices.json'

    @translation.override(None)
    def get_data(self, **options):
        return {
            prop: [
                {'value': value, 'label': f'{label}'}
                for value, label in choices
            ] for prop, choices in self.PROPERTIES
        }
