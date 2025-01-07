import datetime

from celery.signals import worker_shutting_down

from django.db import models, transaction
from django.utils.timezone import localtime

from sentry_sdk import capture_exception

from swp.celery import app
from swp.db.expressions import MakeInterval
from swp.models import Scraper
from swp.utils.scraping.exceptions import ResolverError

SECOND = 1
MINUTE = SECOND * 60
HOUR = MINUTE * 60

HARD_TIME_LIMIT = 6 * HOUR
SOFT_TIME_LIMIT = HARD_TIME_LIMIT - MINUTE


@app.task(name='scraper.schedule')
def schedule_scrapers(now=None):
    now = localtime(now)
    start = now.replace(minute=0, second=0, microsecond=0)
    end = start + datetime.timedelta(hours=1)
    queryset = Scraper.objects.annotate(
        next_run=models.Case(
            models.When(last_run=None, then=now),
            default=models.ExpressionWrapper(
                models.F('last_run') + MakeInterval(hours=models.F('interval')),
                output_field=models.DateTimeField(default=None),
            ),
        ),
    ).filter(
        thinktank__is_active=True,
        is_active=True,
        is_running=False,
        next_run__lt=end,
    )

    for scraper in queryset:
        run_scraper.apply_async(args=[scraper.id], eta=scraper.next_run)

    return len(queryset)


@app.task(name='scraper.run', time_limit=HARD_TIME_LIMIT, soft_time_limit=SOFT_TIME_LIMIT)
def run_scraper(scraper, *, now: datetime.datetime = None, using: str = None, force: bool = False):
    queryset = Scraper.objects.using(using).select_related('thinktank')

    with transaction.atomic(using=using):
        try:
            scraper = queryset.get_for_update(id=scraper)
        except Scraper.DoesNotExist:
            return None

        if skip(scraper, force, now):
            return None

        scraper.errors.all().delete()
        scraper.update(is_running=True)

    try:
        return scraper.scrape()
    except Exception as error:
        scraper.errors.create(message=f'{error}')

        if not isinstance(error, ResolverError):
            capture_exception(error)
    finally:
        scraper.update(last_run=localtime(None), is_running=False, modified=False)


def skip(scraper: Scraper, force: bool = False, now: datetime.datetime = None):
    return False if force else scraper.is_running or scraper.next_run > localtime(now)


@worker_shutting_down.connect
def stop_scrapers(sender, **kwargs):
    if count := Scraper.objects.filter(is_running=True).update(is_running=False):
        print(f'Stopped {count} running scraper(s).')
    else:
        print('No scrapers running.')
