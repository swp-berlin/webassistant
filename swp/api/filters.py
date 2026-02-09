from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter

from swp.utils.compat import removeprefix
from swp.utils.text import enumeration


class SWPOrderingError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('The following fields are not supported for ordering: %s')
    default_code = 'ordering'

    def __init__(self, fields):
        super().__init__(self.default_detail % enumeration(fields))


class SWPOrderingFilter(OrderingFilter):

    def get_valid_ordering_fields(self, queryset, view, request):
        return {name for name, label in self.get_valid_fields(queryset, view, context={'request': request})}

    def remove_invalid_fields(self, queryset, fields, view, request):
        valid_fields = self.get_valid_ordering_fields(queryset, view, request)
        used_fields = {removeprefix(field, '-') for field in fields}

        if invalid_fields := used_fields - valid_fields:
            raise SWPOrderingError(invalid_fields)

        return fields
