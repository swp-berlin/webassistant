from unittest.mock import patch

from django.conf import settings
from django.test import TestCase

from requests import ConnectTimeout

from swp.models import Publication
from swp.utils.requests import TimeOutSession
from swp.utils.spooling import spool_content
from swp.utils.tempdir import maketempdir
from swp.utils.testing import (
    FakeResponse,
    call_command,
    create_publication,
    create_thinktank,
    get_random_embedding_vector,
)


class ManagementCommandTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.thinktank = thinktank = create_thinktank()
        cls.publication = create_publication(thinktank)

    def test_process_embeddings(self):
        embedding = get_random_embedding_vector(settings.EMBEDDING_VECTOR_DIMS)

        with maketempdir(prefix='spooling') as tempdir:

            # No files to process…
            call_command('process-embeddings', directory=tempdir)

            # Fill spooling dir…
            spool_content(self.publication, 'Test', 'txt', tempdir)
            spool_content(Publication(id=self.publication.id - 1), 'Does not Exist', 'txt', tempdir)
            spool_content(create_publication(self.thinktank, embedding=embedding), 'Already Embedded', 'txt', tempdir)
            spool_content(create_publication(self.thinktank), 'No Content', 'txt', tempdir)
            spool_content(create_publication(self.thinktank), 'Bad Request', 'txt', tempdir)
            spool_content(create_publication(self.thinktank), 'Bad Gateway', 'txt', tempdir)
            spool_content(create_publication(self.thinktank), 'Network Error', 'txt', tempdir)

            def results():
                yield None, ConnectTimeout('The request timed out.')
                yield True, embedding
                yield True, None
                yield False, FakeResponse(502)
                yield False, FakeResponse(400)

                while True:
                    yield None, ConnectTimeout('The request timed out.')

            with patch.object(TimeOutSession, 'json', side_effect=results()):
                with patch('time.sleep'):
                    call_command('process-embeddings', directory=tempdir, keep_done=False)
