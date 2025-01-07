import datetime

from celery import group

from django.db.models import Q, F
from django.utils.timezone import localtime

from swp.celery import app
from swp.models import Publication
from swp.utils.marc21 import Record, get_publication_id, get_publication_date, get_authors
from swp.utils.pollux import PolluxAPI, RecordDoesNotExist

SCHEDULE_LIMIT = 60 * 60
RETRY_DELAY = datetime.timedelta(hours=24)
INITIAL_DELAY = datetime.timedelta(hours=24)


@app.task(name='pollux.schedule')
def schedule(*, using: str = None, now: datetime.datetime = None):
    queryset = get_schedule_queryset(using, now)
    publications = queryset.values_list('id', flat=True)[:SCHEDULE_LIMIT]
    tasks = group(fetch.s(publication_id) for publication_id in publications).delay(using=using)

    return len(tasks)


def get_schedule_queryset(using: str = None, now: datetime.datetime = None):
    now = localtime(now)
    retry = now - RETRY_DELAY
    initial = now - INITIAL_DELAY

    return Publication.objects.using(using).filter(
        Q(last_pollux_fetch=None) | Q(last_pollux_fetch__lt=retry),
        last_pollux_update=None,
        created__lt=initial,
    ).order_by(
        F('last_pollux_fetch').asc(nulls_first=True),
        'created',
    )


@app.task(name='pollux.fetch', rate_limit='1/s')
def fetch(publication_id: int, *, using: str = None, now: datetime.datetime = None):
    now = localtime(now)
    queryset = Publication.objects.using(using).filter(id=publication_id)

    if queryset.update(last_pollux_fetch=now) == 0:
        return f'Publication with id {publication_id} does not exist.'

    try:
        record = PolluxAPI.record(f'swp-{publication_id}')
    except RecordDoesNotExist as error:
        return f'{error}'
    else:
        return update(record, publication_id, using=using, now=now)


@app.task(name='pollux.update')
def update(record: Record, publication_id: int = None, *, using: str = None, now: datetime.datetime = None):
    publication_id = publication_id or get_publication_id(record)

    if publication_id is None:
        return 'No associated publication id found.'

    now = localtime(now)
    updates = {'last_pollux_fetch': now, 'last_pollux_update': now}

    if publication_date := get_publication_date(record):
        updates['publication_date_clean'] = publication_date

    if authors := get_authors(record):
        updates['authors'] = authors

    try:
        publication = Publication.objects.using(using).get(id=publication_id)
    except Publication.DoesNotExist:
        return f'Publication with id {publication_id} does not exist.'

    publication.update(**updates)

    return f'Updated publication {publication_id}.'


@app.task(name='pollux.update-all', rate_limit='1/s')
def update_all(query, *, using: str = None, **params):
    """
    Currently unused but might come in handy.
    """

    records, next_record_position = PolluxAPI.records(query, **params)

    if records:
        group(update.s(record) for record in records).delay(using=using)

    if next_record_position:
        params['startRecord'] = next_record_position

        update_all.delay(using=using, **params)

    return len(records)
