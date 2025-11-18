from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

from rest_framework.serializers import CharField


@extend_schema_field(OpenApiTypes.HOSTNAME)
class DomainField(CharField):
    pass
