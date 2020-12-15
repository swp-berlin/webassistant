from django.utils import translation

from swp.management.scheme import GenerateSchemeCommand
from swp.models.choices import Interval, ScraperType


class Command(GenerateSchemeCommand):
    PROPERTIES = [
        ('ScraperType', ScraperType.choices),
        ('interval', Interval.choices),
        # ('country', countries),
        # ('language', settings.LANGUAGES),
        # ('salutation', Patient.Salutations.choices),
        # ('score', BaseAssessment.Score.choices),
        # ('ingestions', TimeChoices.choices),
        # ('PatientFilter', PatientFilter.FILTER_CHOICES.choices),
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
