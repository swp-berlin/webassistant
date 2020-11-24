import os

from django.conf import settings
from django.core.management import BaseCommand
from django.template import Template, Context
from django.utils import translation
from django.utils.encoding import force_text
from django.views.i18n import JavaScriptCatalog

TEMPLATE = r"""
{% load format %}
(function (django, catalog) {
    django.catalog = django.catalog || {};
    Object.keys(catalog).forEach(function (key) {
        django.catalog[key] = catalog[key];
    });
}(django, {{ catalog|json }}));
"""


class JavaScriptCatalogExtension(JavaScriptCatalog):

    def render_to_response(self, context, **response_kwargs):
        template = Template(TEMPLATE)
        context = Context(context)

        return template.render(context)


class Command(BaseCommand):
    packages = [
        'swp',
        'cosmogo',
    ]

    def add_arguments(self, parser):
        parser.add_argument('--directory', dest='directory', default=settings.BASE_DIR / 'swp' / 'assets' / 'i18n')

    def handle(self, *, directory, **options):
        os.makedirs(directory, exist_ok=True)

        catalog_view = JavaScriptCatalog(packages=self.packages)
        extension_view = JavaScriptCatalogExtension(domain='django')

        for code, name in settings.LANGUAGES:
            self.stdout.write(f'Generating JavaScript translation catalog for {code}…')

            with translation.override(code):
                response = catalog_view.get(None)
                extension = extension_view.get(None)
                catalog = force_text(response.content)

                with open(directory / f'{code}.js', 'w') as fp:
                    fp.write(catalog)
                    fp.write(extension)
