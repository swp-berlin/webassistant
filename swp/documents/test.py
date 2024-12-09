from unittest import skipUnless

from django.conf import settings
from django.test import TestCase

from swp.models import Category, Publication, Thinktank, Pool
from swp.utils.testing import call_command


class PublicationDocumentTestCase(TestCase):

    @skipUnless(settings.TEST_REBUILD_SEARCH_INDEX, 'Rebuilding search index disabled…')
    def test_rebuild_search_index(self):
        pool = Pool.objects.get(id=0)
        category = Category.objects.create(name='Test')
        thinktank = Thinktank.objects.create(name='Test', pool=pool, url='https://example.com')
        publication = Publication.objects.create(thinktank=thinktank, title=thinktank.name, url=thinktank.url)
        publication.categories.add(category)

        call_command('search_index', action='rebuild', force=True)
