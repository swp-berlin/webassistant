from typing import Union

from django.core.exceptions import ValidationError


def get_field_validation_error(field: str,
                               message: Union[ValidationError, str],
                               code: str = None,
                               params: dict = None) -> ValidationError:
    if isinstance(message, ValidationError):
        error = message
    else:
        error = ValidationError(message, code, params)

    return ValidationError({field: [error]})
