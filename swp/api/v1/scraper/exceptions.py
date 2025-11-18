from django.utils.translation import gettext_lazy as _

from swp.api.v1.exceptions import BadRequestException


class ScraperActiveException(BadRequestException):
    default_detail = _('Scraper is active and cannot be changed.')
    default_code = 'active'
