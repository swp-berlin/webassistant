from django.core.management import call_command

from swp.management.scheme import GenerateSchemeCommand


class Command(GenerateSchemeCommand):
    SCHEMES = (
        'choices',
    )

    def handle(self, *, schemes=SCHEMES, **options):
        for scheme in schemes:
            call_command(f'generate-{scheme}-scheme', **options)

    get_data = None
