from pathlib import PurePath
from uuid import UUID

from django.core.serializers.json import DjangoJSONEncoder
from django.utils.functional import Promise

try:
    from django.utils.encoding import force_str
except ImportError:
    from django.utils.encoding import force_text as force_str


class AdvancedJSONEncoder(DjangoJSONEncoder):
    """
    Advanced JSON encoder that could handle common
    data types when working with django.
    """

    TEXT_TYPES = (
        Exception,
        Promise,
        PurePath,
        UUID,
    )

    def default(self, o, texts=TEXT_TYPES):
        """
        Converts exceptions and promises to strings.
        """

        if isinstance(o, texts):
            return force_str(o)

        return super(AdvancedJSONEncoder, self).default(o)
