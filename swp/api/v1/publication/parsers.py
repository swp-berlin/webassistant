from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser


class ElasticSearchQueryParser(JSONParser):

    def parse(self, stream, media_type=None, parser_context=None):
        value = super().parse(stream, media_type=media_type, parser_context=parser_context)

        if isinstance(value, dict):
            return value

        raise ParseError(_('Invalid elastic search query object.'))
