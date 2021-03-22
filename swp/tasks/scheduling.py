import datetime
from typing import Iterable, Optional

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives, get_connection as get_mail_connection
from django.db import models, transaction
from django.utils.timezone import localtime

from sentry_sdk import capture_exception

from cosmogo.utils.mail import render_mail
from cosmogo.utils.url import get_absolute_url
from swp.celery import app
from swp.db.expressions import MakeInterval
from swp.models import Scraper
from swp.utils.auth import get_superuser_email_addresses


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


@app.task(name='scraper.run')
def run_scraper(scraper, now=None, using=None, force=False, silent=False):
    with transaction.atomic(using=using):
        try:
            scraper = Scraper.objects.select_related('thinktank').get_for_update(pk=scraper)
        except Scraper.DoesNotExist:
            return None

        if not force and scraper.is_running:
            return None

        if not force and scraper.next_run > localtime(now):
            return None

        scraper.errors.all().delete()
        scraper.update(is_running=True)

    try:
        return scraper.scrape()
    except Exception as error:
        scraper.errors.create(message=f'{error}')
        capture_exception(error)
    finally:
        scraper.update(last_run=localtime(None), is_running=False)
        if not silent:
            send_scraper_errors(scraper=scraper, force=force)


def get_absolute_scraper_url(scraper: Scraper) -> str:
    args = [scraper.thinktank_id, scraper.pk]
    return get_absolute_url(None, 'thinktank:scraper:edit', *args)


def send_scraper_errors(scraper: Scraper, force: bool = False) -> Optional[int]:
    if not force and scraper.is_running:
        return None

    errors = scraper.errors.error_only()
    if not len(errors):
        return None

    email_addresses = get_superuser_email_addresses()
    if not email_addresses:
        return None

    context = {
        'scraper': scraper,
        'thinktank': scraper.thinktank,
        'url': get_absolute_scraper_url(scraper),
        'errors': errors,
    }

    subject, message, html_message = render_mail('scraper-errors', context=context)
    alternatives = [(html_message, 'text/html')] if html_message else []

    messages = [
        EmailMultiAlternatives(
            subject=subject,
            body=message,
            to=[email],
            alternatives=alternatives,
        ) for email in email_addresses
    ]

    return get_mail_connection().send_messages(messages)

