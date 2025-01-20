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


async def scrape(scraper: Scraper, config: dict) -> dict:
    publications = []

    max_len = configure_preview_pagination(config)
    results = scraper.scrape(config)

    try:
        async for publication in results:
            publications.append(publication)

            if len(publications) == max_len:
                break
    except ScraperError as err:
        return {
            'success': False,
            'error': str(err)
        }
    finally:
        # we explicitly have to await closing of the generator
        # otherwise it will not be correctly finalized
        # see https://stackoverflow.com/q/66349410/5005177
        await results.aclose()

    max_per_page = config['paginator']['max_per_page']
    is_multipage = len(publications) > max_per_page

    clean_publications(publications)

    return {
        'success': True,
        'publications': publications,
        'max_per_page': max_per_page,
        'is_multipage': is_multipage,
    }

def clean_publications(publications):
    for publication in publications:
        if fields := publication.get('fields'):
            for embedding_field in ['pdf_path', 'text_content']:
                fields.pop(embedding_field, None)


@app.task(name='preview.scraper')
def preview_scraper(start_url, config):
    scraper = Scraper(start_url)

    result = async_to_sync(scrape)(scraper, config)

    return result
