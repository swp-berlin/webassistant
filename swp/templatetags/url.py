from django import template
from django.contrib.staticfiles.storage import staticfiles_storage

from swp.utils.translation import get_language
from swp.utils.url import get_absolute_url

register = template.Library()


@register.simple_tag(name='absolute_url', takes_context=True)
def absolute_url_tag(context, view_name, *args, **kwargs):
    return get_absolute_url(context.get('request'), view_name, *args, **kwargs)


@register.simple_tag(name='js_catalog_url', takes_context=True)
def js_catalog_url_tag(context, language=None):
    request = context.get('request')
    language = get_language(language, request=request)

    return staticfiles_storage.url(f'i18n/{language}.js')
