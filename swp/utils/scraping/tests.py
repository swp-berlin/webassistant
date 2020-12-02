import asyncio
from unittest import skip

from django.test import SimpleTestCase

from swp.utils.scraping.paginators import PaginatorType
from swp.utils.scraping.resolvers import ResolverType
from swp.utils.scraping.scraper import Scraper


class ScraperTestCase(SimpleTestCase):

    @skip('Run this manually')
    def test_piie(self):
        resolver_config = {
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

        scraper = Scraper(url='https://www.piie.com/research/publications/policy-briefs')

        scraped = asyncio.run(scraper.scrape(resolver_config))

        self.assertEqual(len(scraped), 20)

    @skip('Run this manually')
    def test_brookings(self):
        resolver_config = {
            'type': ResolverType.List,
            'selector': 'article.report',
            'paginator': {
                'type': PaginatorType.Page,
                'list_selector': '.list-content',
                'item_selector': 'article.report',
                'button_selector': '.load-more-link a.load-more',
                'max_pages': 1,
            },
            'resolvers': [
                {'type': ResolverType.Data, 'key': 'type', 'selector': '.article-info .label'},
                {'type': ResolverType.Link, 'selector': '.article-info .title a', 'same_site': True, 'resolvers': [
                    {'type': ResolverType.Attribute, 'key': 'title', 'selector': 'head > meta[property="og:title"]', 'attribute': 'content'},
                    {'type': ResolverType.Attribute, 'key': 'publication_date', 'selector': 'head > meta[property="article:published_time"]', 'attribute': 'content'},
                    # {'type': ResolverType.Document, 'key': 'pdf', 'selector': 'div.download a'}
                ]}
            ]
        }

        scraper = Scraper(url='https://www.brookings.edu/search/?s=&post_type=book&post_type=essay&post_type=research&topic=&pcp=&date_range=&start_date=&end_date=')

        scraped = asyncio.run(scraper.scrape(resolver_config))

        self.assertEqual(len(scraped), 30)

    @skip('Run this manually')
    def test_giga_hamburg(self):
        resolver_config = {
            'type': ResolverType.List,
            'selector': '.l__content .list__item',
            'paginator': {
                'type': PaginatorType.Page,
                'list_selector': '.l__content',
                'item_selector': '.list__item',
                'button_selector': '.pager .next a',
                'max_pages': 1,
            },
            'resolvers': [
                {'type': ResolverType.Data, 'key': 'author', 'selector': '.listing-body .authors'},
                {'type': ResolverType.Link, 'selector': '.list__title a', 'same_site': True, 'resolvers': [
                    {'type': ResolverType.Attribute, 'key': 'title', 'selector': 'head > meta[name="citation_title"]', 'attribute': 'content'},
                    {'type': ResolverType.Attribute, 'key': 'publication_date', 'selector': 'head > meta[name="citation_publication_date"]', 'attribute': 'content'},
                    # {'type': ResolverType.Document, 'key': 'pdf', 'selector': 'a.pdf-download'}
                ]}
            ]
        }

        scraper = Scraper(url='https://www.giga-hamburg.de/de/publikationen/working-papers')

        scraped = asyncio.run(scraper.scrape(resolver_config))

        self.assertEqual(len(scraped), 200)
