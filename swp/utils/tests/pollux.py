from io import BytesIO

from unittest.mock import patch

from django.test import TestCase

from requests import Response

from swp.utils.marc21 import get_authors, get_publication_id, get_publication_date
from swp.utils.pollux import PolluxAPI, ContentTypeMismatch
from swp.utils.testing import get_pollux_response


def get_body(name: str, context: dict = None) -> bytes:
    return get_pollux_response(name, context).encode('utf-8')


class ContentResponse(Response):

    def __init__(self, content: bytes, content_type: str, status_code=200):
        Response.__init__(self)

        self.raw = BytesIO(content)
        self.status_code = status_code
        self.headers['Content-Type'] = content_type


class PolluxResponse(ContentResponse):

    def __init__(self, name, context: dict = None):
        ContentResponse.__init__(self, get_body(name, context), 'text/xml')


class PolluxTestCase(TestCase):

    def test_records(self):
        response = PolluxResponse('real')

        with patch.object(PolluxAPI.session, 'get', return_value=response):
            records, next_record_position = PolluxAPI.records('source:swp')

        self.assertEqual(len(records), 15)
        self.assertEqual(next_record_position, 16)

        record = records[3]
        authors = get_authors(record)

        self.assertEqual(len(authors), 3)

    def test_content_type_mismatch(self):
        response = ContentResponse(b'invalid', 'text/plain')

        with self.assertRaises(ContentTypeMismatch):
            with patch.object(PolluxAPI.session, 'get', return_value=response):
                PolluxAPI.records('source:swp')

    def test_empty_publication_id(self):
        publication_id = get_publication_id({})

        self.assertIsNone(publication_id)

    def test_empty_publication_date(self):
        publication_date = get_publication_date({})

        self.assertIsNone(publication_date)

    def test_empty_authors(self):
        authors = get_authors({})

        self.assertIsInstance(authors, list)
        self.assertFalse(authors)
