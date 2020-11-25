from django.core.management import call_command

from cosmogo.commands.gettext import CompileTranslationsCommand


class Command(CompileTranslationsCommand):
    APPLICATION = 'swp'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--no-catalog', dest='catalog', action='store_false')

    def handle(self, *, catalog=True, **options):
        super(Command, self).handle(**options)

        if catalog:
            call_command('generate-translation-catalogs')
