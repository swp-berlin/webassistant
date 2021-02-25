import copy
from django import test

from swp.tasks.scraper import configure_preview_pagination
from swp.utils.scraping.resolvers import PaginatorType, ResolverType


class PreviewPaginationTestCase(test.TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.resolver_config_1 = {
            'type': ResolverType.List,
            'selector': '.node--publication',
            'paginator': {
                'type': PaginatorType.Page,
                'list_selector': '.view-content',
                'button_selector': '.pager .pager-next a',
                'max_pages': 1,
            },
            'resolvers': [
                {'type': ResolverType.Data, 'key': 'type', 'selector': '.field--publication-type'},
                {'type': ResolverType.Link, 'selector': '.field--title a', 'resolvers': [
                    {'type': ResolverType.Data, 'key': 'title', 'selector': '.field--title'},
                    {'type': ResolverType.Data, 'key': 'author', 'selector': '.field--contributor'},
                    {'type': ResolverType.Data, 'key': 'publication_date', 'selector': '.field--date'},
                ]}
            ]
        }

        cls.resolver_config_2 = copy.deepcopy(cls.resolver_config_1)
        cls.resolver_config_2['paginator']['max_pages'] = 2

        cls.resolver_config_3 = copy.deepcopy(cls.resolver_config_1)
        cls.resolver_config_3['paginator']['max_pages'] = 3

    def test_min_preview_items(self):
        max_len = configure_preview_pagination(self.resolver_config_1)
        self.assertEqual(max_len, 3)

    def test_two_preview_items(self):
        max_len = configure_preview_pagination(self.resolver_config_2)
        self.assertEqual(max_len, 6)

    def test_max_preview_items(self):
        max_len = configure_preview_pagination(self.resolver_config_3)
        self.assertEqual(max_len, 6)

