import datetime

from django.db import models, transaction
from django.utils.timezone import localtime

from swp.celery import app
from swp.db.expressions import MakeInterval
from swp.models import Scraper


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
        is_active=True,
        is_running=False,
        next_run__lt=end,
    )

    for scraper in queryset:
        run_scraper.apply_async(args=[scraper.id], eta=scraper.next_run)

    return len(queryset)


@app.task(name='scraper.run')
def run_scraper(scraper, now=None, using=None):
    with transaction.atomic(using=using):
        try:
            scraper = Scraper.objects.get_for_update(pk=scraper)
        except Scraper.DoesNotExist:
            return None

        if scraper.is_running:
            return None

        if scraper.next_run > localtime(now):
            return None

        scraper.update(is_running=True)

    try:
        return scraper.scrape()
    finally:
        scraper.update(last_run=localtime(None), is_running=False)
