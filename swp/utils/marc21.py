import datetime

from contextlib import suppress
from typing import Dict, List, Optional, Union
from xml.etree.ElementTree import Element

Value = str
SubfieldValue = Dict[str, Value]
DataFieldValue = Union[SubfieldValue, List[SubfieldValue], List[Value], Value]
Record = Dict[str, DataFieldValue]
Records = List[Record]

NAMESPACE = 'marc'
NAMESPACES = {
    NAMESPACE: 'https://www.loc.gov/MARC21/slim',
}

DATAFIELD = 'datafield'
SUBFIELD = 'subfield'

MARC21_CONTROL_NUMBER = '001'
MARC21_MAIN_AUTHOR_NAME = '100', 'a'
MARC21_ADDITIONAL_AUTHOR_NAME = '700', 'a'
MARC21_PUBLICATION_DATE = '260', 'c'


def findall(element, field):
    return element.findall(f'{NAMESPACE}:{field}', NAMESPACES)


def datafields(record) -> Record:
    data = {}

    for field in findall(record, DATAFIELD):
        tag = field.attrib['tag']

        if subfields := findall(field, SUBFIELD):
            value = {subfield.attrib['code']: subfield.text for subfield in subfields}
        else:
            value = field.text

        if tag in data:
            if isinstance(data[tag], list):
                data[tag].append(value)
            else:
                data[tag] = [data[tag], value]
        else:
            data[tag] = value

    return data


def get_records(content: Element) -> Records:
    if records := content.find('records'):
        if records := records.findall('record'):  # pragma: no branch
            return [datafields(record) for record in records]

    return []


def get_value(record: Record, identifier):
    if isinstance(identifier, str):
        tag, code = identifier, None
    else:
        tag, code = identifier

    with suppress(KeyError):
        return select_value(record[tag], code)


def select_value(value: DataFieldValue, code: str = None):
    if isinstance(value, dict):
        return value[code]

    if isinstance(value, list):
        return [select_value(value, code) for value in value]

    return value


def ensure_list(value: Union[List[str], str, None]) -> List[str]:
    if value is None:
        return []

    if isinstance(value, list):
        return value

    return [value]


def get_publication_id(record: Record) -> Optional[int]:
    if value := get_value(record, MARC21_CONTROL_NUMBER):
        prefix, number = value.split('-')

        return int(number)


def get_publication_date(record: Record) -> Optional[datetime.date]:
    if value := get_value(record, MARC21_PUBLICATION_DATE):
        return datetime.datetime.strptime(value, '%Y%m%d').date()


def get_authors(record: Record) -> List[str]:
    author = get_value(record, MARC21_MAIN_AUTHOR_NAME)
    authors = get_value(record, MARC21_ADDITIONAL_AUTHOR_NAME)

    return [*ensure_list(author), *ensure_list(authors)]
