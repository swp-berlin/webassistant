import datetime
import re

from typing import Union, Type

from django.utils import timezone, translation
from django.utils.formats import date_format
from django.utils.dateparse import parse_date, parse_datetime

LANGUAGES = [
    'de',
    'en',
    'es',
    'fr',
    'ru',
    'be',
]

FORMATS = ['M', 'F', 'N', 'b.']


def build_months(months):
    dates = [datetime.date(2000, month + 1, 1) for month in range(12)]

    for language in LANGUAGES:
        with translation.override(language):
            for date in dates:
                for fmt in FORMATS:
                    label = date_format(date, fmt)
                    identifier = str.lower(label)
                    months[identifier] = date.month

    return months


MONTHS = build_months({})
TEXTUAL_MONTH_PATTERN = '|'.join(map(re.escape, MONTHS))

datetime_patterns = [
    r'(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<year>\d{2}) (?P<hour>\d{2}):(?P<minute>\d{2})',
    (r'(?P<year>\d{2})-(?P<month>\d{1,2})-(?P<day>\d{1,2})T'
     r'(?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2})(?P<tz>Z)'),
]

date_patterns = [
    r'(?P<day>\d{1,2})[/\.-](?P<month>\d{1,2})[/\.-](?P<year>\d{4})',
    r'(?P<year>\d{4})[/\.-](?P<month>\d{1,2})[/\.-](?P<day>\d{1,2})',
    r'(?P<day>\d{1,2})/(?P<month>\d{1,2})/(?P<year>\d{2,4})',
    r'(?P<month>%s) (?P<day>\d{1,2}),? (?P<year>\d{4})' % TEXTUAL_MONTH_PATTERN,
    r'(?P<day>\d{1,2})(\.|th)? ?(?P<month>%s) (?P<year>\d{4})' % TEXTUAL_MONTH_PATTERN,
]

fractional_patterns = [
    r'(?P<month>\d{1,2})[/\.](?P<year>\d{4})',
    r'(?P<day>\d{1,2}) (?P<month>%s)' % TEXTUAL_MONTH_PATTERN,
    r'(?P<month>%s) (?P<year>\d{4})' % TEXTUAL_MONTH_PATTERN,
    r'(?P<year>(19|20)\d{2})',
]

relative_patterns = [
    r'(?P<hours>\d+) hours ago',
    r'(?P<minutes>\d+) min ago',
]

PATTERNS = [
    (datetime.datetime, datetime_patterns),
    (datetime.date, date_patterns),
    (dict, fractional_patterns),
    (datetime.timedelta, relative_patterns),
]


def parse_publication_date(value):
    value = ' '.join(value for value in str.split(value) if value)

    if publication_date := parse_datetime(value):
        return publication_date

    if publication_date := parse_date(value):
        return publication_date

    for builder, patterns in PATTERNS:
        for pattern in patterns:
            if match := re.search(pattern, value, re.IGNORECASE | re.UNICODE):
                return build(builder, match)


Builder = Union[
    Type[dict],
    Type[datetime.date],
    Type[datetime.datetime],
    Type[datetime.timedelta],
]


def build(builder: Builder, match: re.Match):
    bits = match.groupdict()
    tzinfo = bits.pop('tz', None)

    for key, value in bits.items():
        try:
            bits[key] = int(value)
        except ValueError:
            value = str.lower(value)
            bits[key] = MONTHS.get(value)

    if bits.get('month', 0) > 12:
        bits['day'], bits['month'] = bits['month'], bits['day']

    if tzinfo == 'Z':
        bits['tzinfo'] = timezone.utc

    return builder(**bits)
