from django.utils import translation

from swp.management.scheme import GenerateSchemeCommand
from swp.models.choices import (
    DataResolverKey,
    Interval,
    ListResolverType,
    PaginatorType,
    ResolverType,
    UniqueKey,
)


class Command(GenerateSchemeCommand):
    PROPERTIES = [
        ('interval', Interval.choices),
        ('ResolverType', ResolverType.choices),
        ('ListResolverType', ListResolverType.choices),
        ('DataResolverKey', DataResolverKey.choices),
        ('UniqueKey', UniqueKey.choices),
        ('PaginatorType', PaginatorType.choices),
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
