from django.urls.converters import StringConverter
from django.utils.dateparse import parse_date


class DateConverter(StringConverter):
    regex = '[0-9]{1,4}-[0-9]{2}-[0-9]{2}'

    def to_python(self, value: str):
        return parse_date(value)

    def to_url(self, value):
        if isinstance(value, str):
            value = parse_date(value)

        return value.isoformat()
