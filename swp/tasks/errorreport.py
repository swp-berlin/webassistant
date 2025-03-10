from django.contrib.postgres.aggregates import ArrayAgg
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.db.models import Prefetch
from django.utils.timezone import localtime

from swp.celery import app
from swp.models import ErrorLevel, Pool, Publication, Scraper, ScraperError, Thinktank
from swp.utils.auth import get_user_queryset
from swp.utils.defaultdict import NestedDefaultDict
from swp.utils.mail import render_mail
from swp.utils.text import when


@app.task(name='error-report.send')
def send_scraper_errors(*, using: str = None):
    connection = mail.get_connection(fail_silently=True)

    with transaction.atomic(using):
        queryset, pools = collect_scraper_errors(using)

        if not pools:
            return 0

        recipients = get_recipients(pools)
        messages = [get_message(recipient, pools) for recipient, pools in recipients]
        count = connection.send_messages(messages)
        sent = localtime(None)

        queryset.update(sent=sent)

    return count


def collect_scraper_errors(using: str = None):
    queryset = ScraperError.objects.using(using).prefetch_related(
        Prefetch('publication', Publication.objects.only('title', 'url')),
        Prefetch('scraper', Scraper.objects.only('thinktank').prefetch_related(
            Prefetch('thinktank', Thinktank.objects.only('name', 'pool').prefetch_related(
                Prefetch('pool', Pool.objects.only('name')),
            )),
        )),
    ).filter(
        level=ErrorLevel.ERROR,
        sent=None,
    ).order_by(
        'scraper__thinktank__pool__name',
        'scraper__thinktank__pool_id',
        'scraper__thinktank__name',
        'scraper__thinktank_id',
        'scraper',
    )

    pools = NestedDefaultDict(list, 3)

    for error in queryset.select_for_update(nowait=False):
        scraper = error.scraper
        thinktank = scraper.thinktank
        pool = thinktank.pool
        key = '-'.join(when([error.code, error.field])) or 'general'

        pools[pool][thinktank][scraper][key].append(error)
        pool.error_count = getattr(pool, 'error_count', 0) + 1

    return queryset, pools.dict


def get_recipients(pools):
    queryset = get_user_queryset(
        is_active=True,
        is_error_recipient=True,
    ).exclude(
        email='',
    ).annotate(
        user_pool_ids=ArrayAgg('pools'),
    ).values_list(
        'email',
        'user_pool_ids',
    )

    for email, user_pool_ids in queryset:
        user_pool_ids = {*user_pool_ids}

        if user_pool_ids == {None}:
            user_pools = pools
        else:
            user_pools = {pool: thinktanks for pool, thinktanks in pools.items() if pool.id in user_pool_ids}

        if user_pools:
            yield email, user_pools


def get_message(recipient, pools):
    subject, plain, html = render_mail('scraper-errors', context={'pools': pools})

    return EmailMultiAlternatives(
        to=[recipient],
        subject=subject,
        body=plain,
        alternatives=[
            (html, 'text/html'),
        ],
    )
