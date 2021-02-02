from asgiref.sync import async_to_sync

from swp.celery import app
from swp.utils.scraping import Scraper
from swp.utils.scraping.exceptions import ScraperError


PUBLICATION_PREVIEW_COUNT = 3


async def scrape(scraper, config):
    publications = []

    try:
        async for publication in scraper.scrape(config):
            publications.append(publication)

            if len(publications) == PUBLICATION_PREVIEW_COUNT:
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
