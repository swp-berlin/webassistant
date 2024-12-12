import os
import polib

from django.core.management import BaseCommand, call_command

from swp.utils.path import cd
from swp.utils.translation import GetTextCommandMixin


class Command(GetTextCommandMixin, BaseCommand):
    requires_system_checks = []

    APPLICATION = 'swp'

    IGNORE = [
        'static',
        'test-data',
        'assets/i18n',
    ]

    DOMAINS = [
        ('django', [
            'html', 'txt', 'py',  # default
            'plain', 'subject',  # mails
        ]),
        ('djangojs', None),
    ]

    META = {
        'Content-Type',
        'Plural-Forms',
        'Language',
    }

    WRAP_WIDTH = 0  # no wrap

    def add_arguments(self, parser):
        parser.add_argument('-l', dest='languages', action='append', choices=self.language_codes)
        parser.add_argument('-d', dest='domains', action='append', choices=list(dict(self.DOMAINS)))

    def handle(self, languages, domains, **options):
        """
        Creates and cleans the translation files
        for every domain and configured language.
        """

        # We will create translation files
        # in the app dir and not globally.
        with cd(self.APPLICATION):
            return self.run(languages, domains, **options)

    def run(self, languages, domains, **options):
        # The locale dir isn't created automatically by makemessages.
        os.makedirs(self.LOCALE_DIR, exist_ok=True)

        languages = self.get_languages(languages)
        domains = self.get_domains(domains)

        for domain, extensions in domains:
            self.call_command(
                locale=languages,
                domain=domain,
                extensions=extensions,
                ignore_patterns=self.IGNORE,
                no_wrap=self.WRAP_WIDTH == 0,
                no_location=True,
                symlinks=True,
                **options
            )

        for language in languages:
            for domain, extensions in domains:
                self.clean(language, domain)

    def get_languages(self, languages):
        """
        When no language is given assume all languages.
        """

        return languages or self.language_codes

    def get_domains(self, domains):
        """
        Assume all extensions for given domains.
        """

        return domains and [(domain, None) for domain in domains] or self.DOMAINS

    @staticmethod
    def call_command(**kwargs):
        kwargs.pop('skip_checks', None)  # makemessages doesn't take this argument

        return call_command('makemessages', **kwargs)

    @classmethod
    def clean(cls, language, domain):
        """
        We use the polib library to parse the output
        file and remove all unnecessary meta data.
        """

        filepath = cls.get_filepath(language, domain)

        if not os.path.isfile(filepath):
            return False

        pofile = polib.pofile(filepath, wrapwidth=cls.WRAP_WIDTH)

        cls.set_meta_language(pofile, language)
        cls.set_header(pofile, language, domain)

        for key in list(pofile.metadata):
            if key not in cls.META:
                pofile.metadata.pop(key)

        pofile.save(filepath)

        return True

    @staticmethod
    def set_meta_language(pofile, language, key='Language'):
        if not pofile.metadata.get(key):
            pofile.metadata[key] = language

    @classmethod
    def set_header(cls, pofile, language, domain):
        language = pofile.metadata.get('Language', language)
        domain = 'frontend' if 'js' in domain else 'backend'
        pofile.header = f'{language} translations for {domain} code'
