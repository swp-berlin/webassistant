import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, URLValidator
from django.utils.translation import gettext_lazy as _

from swp.utils.domain import get_canonical_domain

validate_domain = RegexValidator(
    regex=rf'^{URLValidator.hostname_re}{URLValidator.domain_re}{URLValidator.tld_re}$',
    flags=re.IGNORECASE,
    message=_('Please enter a valid domain.'),
    code='invalid',
)


def validate_canonical_domain(value: str):
    validate_domain(value)

    domain = get_canonical_domain(value)

    if value == domain:
        return value

    raise ValidationError(
        message=_(
            'The entered domain is not a canonical domain. '
            'The canonical domain to the entered domain is: %(domain)s'
        ),
        params={'domain': domain},
        code='not-canonical',
    )
