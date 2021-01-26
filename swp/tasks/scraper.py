from asgiref.sync import async_to_sync

from swp.celery import app
from swp.utils.scraping import Scraper


PUBLICATION_PREVIEW_COUNT = 3


async def scrape(scraper, config):
    publications = []

    async for publication in scraper.scrape(config):
        publications.append(publication)

        if len(publications) == PUBLICATION_PREVIEW_COUNT:
            break

    return publications


@app.task(name='preview.scraper')
def preview_scraper(start_url, config):
    scraper = Scraper(start_url)

    publications = async_to_sync(scrape)(scraper, config)

    return publications
