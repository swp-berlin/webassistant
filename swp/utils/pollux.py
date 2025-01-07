from urllib.parse import urlsplit, urlunsplit, parse_qs
from xml.etree import ElementTree

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.utils.http import urlencode

from requests import RequestException

from swp.utils.marc21 import get_records
from swp.utils.requests import TimeOutSession, get_content_type


class ContentTypeMismatch(RequestException):
    pass


class RecordDoesNotExist(ObjectDoesNotExist):
    pass


class MultipleRecordsReturned(MultipleObjectsReturned):
    pass


class PolluxAPI:

    def __init__(self, host, version=2.0):
        self.host = host
        self.version = version
        self.session = TimeOutSession(30)

    def get_url(self, endpoint, **params):
        params.setdefault('version', self.version)

        scheme, netloc, path, query, fragment = urlsplit(self.host)
        query = urlencode({**parse_qs(query), **params}, doseq=True)
        components = scheme, netloc, f'/api/{endpoint}', query, fragment

        return urlunsplit(components)

    def sru(self, **params):
        url = self.get_url('sru', **params)

        with self.session.get(url) as response:
            response.raise_for_status()

            if get_content_type(response) == 'text/xml':
                return ElementTree.fromstring(response.text)

            raise ContentTypeMismatch('Response is not XML.', response=response)

    def record(self, record_id: str, **params):
        params['query'] = f'id:{record_id}'
        params['maximumRecords'] = 2

        records, _ = self.records(**params)

        if len(records) == 0:
            raise RecordDoesNotExist(f'Record with id {record_id} does not exist.')
        elif len(records) > 1:
            raise MultipleRecordsReturned(f'More than one record with id {record_id} returned.')

        return records[0]

    def records(self, query: str, **params):
        params['query'] = query

        params.setdefault('operation', 'searchRetrieve')
        params.setdefault('maximumRecords', 100)

        content = self.sru(**params)

        next_record_position = content.find('nextRecordPosition')

        if next_record_position is not None:
            next_record_position = int(next_record_position.text)

        return get_records(content), next_record_position


PolluxAPI: PolluxAPI = PolluxAPI('https://www.pollux-fid.de')
