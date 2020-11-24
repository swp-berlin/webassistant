import json

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

from cosmogo.encoder import AdvancedJSONEncoder

register = template.Library()


@register.filter(name='json')
def json_filter(value, cls=AdvancedJSONEncoder):
    try:
        dumped = json.dumps(value, cls=cls)
    except (ValueError, TypeError, OverflowError):
        if settings.DEBUG:  # pragma: no cover
            raise
        else:
            dumped = 'undefined'

    return mark_safe(dumped)
