from cssselect import SelectorSyntaxError, parse
from rest_framework.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _


def css_selector(value: str):
    try:
        parse(value)
    except SelectorSyntaxError:
        raise ValidationError(detail=_('Invalid Selector'), code='invalid-selector')
