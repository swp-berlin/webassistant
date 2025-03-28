from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import APIException, ErrorDetail
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_503_SERVICE_UNAVAILABLE
from rest_framework.views import exception_handler as base_exception_handler


class InvalidQueryError(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_code = 'invalid-query'
    default_detail = _('The query provided is invalid. Please check your input.')


class FullTextSearchError(APIException):
    status_code = HTTP_503_SERVICE_UNAVAILABLE
    default_code = 'service-unavailable'
    default_detail = _('The full-text search is currently unavailable. Please try again later.')
    wait = 60


def exception_handler(exception, context):
    response = base_exception_handler(exception, context)

    if can_add_error_code(exception, response):
        response.data.setdefault('code', exception.detail.code or exception.status_code)

    return response


def can_add_error_code(exception, response: Response):
    return (
        isinstance(exception, APIException) and
        isinstance(exception.detail, ErrorDetail) and
        isinstance(response.data, dict)
    )
