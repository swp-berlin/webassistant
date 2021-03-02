from asgiref.sync import async_to_sync

from swp.celery import app
from swp.utils.scraping import Scraper
from swp.utils.scraping.exceptions import ScraperError


PUBLICATION_PREVIEW_COUNT = 3
PUBLICATION_PREVIEW_PAGES = 2


def configure_preview_pagination(config: dict) -> int:
    """ Setup scraper config for limited pagination during preview. """
    paginator = config.pop('paginator', None) or {}
    max_pages = min(paginator.get('max_pages', 1), PUBLICATION_PREVIEW_PAGES)
    max_per_page = paginator.get('max_per_page') or PUBLICATION_PREVIEW_COUNT

    paginator.update(max_pages=max_pages, max_per_page=max_per_page)
    config['paginator'] = paginator

    return max_pages * max_per_page


async def scrape(scraper, config):
    publications = []

    max_len = configure_preview_pagination(config)

    try:
        async for publication in scraper.scrape(config):
            publications.append(publication)

            if len(publications) == max_len:
                break
    except ScraperError as err:
        return {
            'success': False,
            'error': str(err)
        }

    return {
        'success': True,
        'publications': publications,
    }


@app.task(name='preview.scraper')
def preview_scraper(start_url, config):
    scraper = Scraper(start_url)

    result = async_to_sync(scrape)(scraper, config)

    return result
