from django.test import TestCase

from swp.utils.spooling import spool_file, spool_content, iter_files
from swp.utils.tempdir import maketempdir
from swp.utils.testing import create_publication, create_thinktank


class SpoolingTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.thinktank = thinktank = create_thinktank()
        cls.publication = create_publication(thinktank)

    def test_spool_file(self):
        with maketempdir(prefix='spooling') as tempdir:
            source = tempdir / 'test.txt'

            with open(source, 'w') as fp:
                fp.write('test')

            destination = spool_file(self.publication, source, 'txt', directory=tempdir)

            self.assertTrue(source.exists())
            self.assertTrue(destination.exists())

    def test_iter_files(self):
        with maketempdir(prefix='spooling') as tempdir:
            destination = spool_content(self.publication, 'test', 'txt', directory=tempdir)
            files = dict(iter_files(tempdir, 'todo'))

        self.assertIn(self.publication.id, files)
        self.assertEqual(files[self.publication.id], destination)
