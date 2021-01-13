from django.utils import translation

from swp.management.scheme import GenerateSchemeCommand
from swp.models.choices import DataResolverKey, Interval, ResolverType


class Command(GenerateSchemeCommand):
    PROPERTIES = [
        ('interval', Interval.choices),
        ('ResolverType', ResolverType.choices),
        ('DataResolverKey', DataResolverKey.choices)
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
