from django.db.models import ProtectedError
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.exceptions import APIException


class ProtectedErrorException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Object cannot be deleted because it is still referenced.')
    default_code = 'referenced'

    def __init__(self, error: ProtectedError):
        message, protected_objects = error.args
        detail = {
            'message': message,
            'references': [
                {'type': obj._meta.verbose_name, 'id': obj.id, 'name': f'{obj}'}
                for obj in protected_objects
            ],
        }

        super().__init__(detail)
