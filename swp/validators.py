import re

from django.core.validators import RegexValidator, URLValidator
from django.utils.translation import gettext_lazy as _

validate_domain = RegexValidator(
    regex=rf'^{URLValidator.hostname_re}{URLValidator.domain_re}{URLValidator.tld_re}$',
    flags=re.IGNORECASE,
    message=_('Please enter a valid domain.'),
    code='invalid',
)
