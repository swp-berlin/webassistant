from django.core.management import call_command
from django.core.management.commands.compilemessages import Command as CompileMessagesCommand

from swp.utils.path import cd
from swp.utils.translation import GetTextCommandMixin


class Command(GetTextCommandMixin, CompileMessagesCommand):
    APPLICATION = 'swp'

    """
    This command eases the process of compiling translations
    for a project by avoid compiling message files in the
    virtualenv directory.
    """

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--directory', '-d', default=self.APPLICATION)
        parser.add_argument('--no-catalog', dest='catalog', action='store_false')

    def handle(self, *, directory, catalog=True, **options):
        """
        Changes to the application directory before compiling translation files.
        """

        with cd(directory):
            super().handle(**options)

            if catalog:
                call_command('generate-translation-catalogs')
