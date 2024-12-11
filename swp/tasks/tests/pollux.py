from unittest.mock import patch
from xml.etree import ElementTree

from django.test import TestCase

from swp.utils.marc21 import get_records
from swp.utils.pollux import PolluxAPI, MultipleRecordsReturned
from swp.utils.testing import (
    create_publication,
    create_thinktank,
    patched_group_delay,
    get_pollux_response,
)

from swp.tasks import pollux


def get_response(name: str, context: dict = None):
    content = get_pollux_response(name, context)

    return ElementTree.fromstring(content)


class PolluxTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.thinktank = thinktank = create_thinktank('Pollux')
        cls.publication = create_publication(thinktank, created=thinktank.created - pollux.INITIAL_DELAY)

    def test_schedule(self, **defaults):
        defaults['last_pollux_fetch'] = defaults['last_pollux_update'] = self.publication.created

        create_publication(self.thinktank, **defaults)

        with patched_group_delay:
            count = pollux.schedule()

        self.assertEqual(count, 1)

    def test_fetch_invalid_id(self):
        with patch.object(PolluxAPI, 'record') as record:
            pollux.fetch(0)

        self.assertFalse(record.called)

    def test_fetch_record_does_not_exist(self):
        with patch.object(pollux, 'update') as update:
            with patch.object(PolluxAPI, 'sru') as sru:
                sru.return_value = get_response('empty')
                pollux.fetch(self.publication.id)

        self.assertTrue(sru.called)
        self.assertFalse(update.called)

    def test_fetch_multiple_records_returned(self):
        with self.assertRaises(MultipleRecordsReturned):
            with patch.object(PolluxAPI, 'sru') as sru:
                sru.return_value = get_response('two')
                pollux.fetch(self.publication.id)

    def test_fetch_updated(self):
        with patch.object(PolluxAPI, 'sru') as sru:
            sru.return_value = get_response('one', {'id-1': self.publication.id})
            result = pollux.fetch(self.publication.id)

        self.assertEqual(result, f'Updated publication {self.publication.id}.')

    def test_update_does_not_exist(self):
        content = get_response('one', {'id-1': 0})
        [record] = get_records(content)
        result = pollux.update(record)

        self.assertEqual(result, f'Publication with id 0 does not exist.')

    def test_update_no_publication_id(self):
        result = pollux.update({})

        self.assertEqual(result, 'No associated publication id found.')

    @staticmethod
    def helper_update_all(name, context: dict = None):
        with patch.object(pollux.update_all, 'delay') as delay:
            with patched_group_delay as group_delay:
                with patch.object(PolluxAPI, 'sru') as sru:
                    sru.return_value = get_response(name, context)
                    result = pollux.update_all('source:swp')

        return result, delay.called, group_delay.called

    def test_update_all(self):
        result, delay_called, group_delay_called = self.helper_update_all('two', {'id-1': 1, 'id-2': 2})

        self.assertTrue(group_delay_called)
        self.assertTrue(delay_called)
        self.assertEqual(result, 2)

    def test_update_all_empty(self):
        result, delay_called, group_delay_called = self.helper_update_all('empty')

        self.assertFalse(group_delay_called)
        self.assertFalse(delay_called)
        self.assertEqual(result, 0)
