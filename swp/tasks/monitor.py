import datetime
from itertools import groupby
from operator import attrgetter
from typing import Iterable, List, Optional, Union

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection as get_mail_connection
from django.db import transaction
from django.db.models import F, Q
from django.utils import timezone

from sentry_sdk import capture_message, push_scope
from cosmogo.utils.mail import render_mail
from cosmogo.utils.requests import TimeOutSession

from swp.celery import app
from swp.models import Monitor, Publication
from swp.models.zotero import ZoteroTransfer
from swp.utils.collections import chunked
from swp.utils.ris import generate_ris_attachment
from swp.utils.zotero import get_zotero_data, build_zotero_api_url, get_zotero_api_headers, get_zotero_object_key


@app.task(name='monitor.schedule')
def schedule_monitors(now: datetime.datetime = None, dry_run: bool = False, **kwargs) -> int:
    """ Schedule hourly monitor dispatches. """
    now = timezone.localtime(now)

    queryset = Monitor.objects.scheduled_during_next_hour(now)
    count = len(queryset)
    if dry_run:
        return count

    for monitor in queryset:
        monitor_new_publications.apply_async(
            args=(monitor.pk,),
            kwargs=kwargs,
            eta=monitor.next_run,
        )

    return count


@app.task(name='monitor.new-publications')
def monitor_new_publications(monitor_id: int, now: datetime.datetime = None, **kwargs) -> Optional[int]:
    """ Dispatch new monitor publications to all recipients. """
    with transaction.atomic(using=kwargs.get('using')):
        monitor = Monitor.objects.get_for_update(pk=monitor_id)
        if not monitor.is_active:
            return None

        monitor.update_publication_count()
        if not monitor.new_publication_count:
            return None

        return send_monitor_publications(monitor, now=now, exclude_sent=True, **kwargs)


def make_monitor_publication_messages(
    monitor: Monitor,
    publications: Iterable[Publication],
    **kwargs
) -> Iterable[EmailMultiAlternatives]:
    context = {
        'monitor': monitor,
    }

    subject, message, html_message = render_mail('monitor-publications', context=context)
    alternatives = [(html_message, 'text/html')] if html_message else []

    attachment = generate_ris_attachment(monitor.name, publications)

    return [
        EmailMultiAlternatives(
            subject=subject,
            body=message,
            to=[email],
            attachments=[attachment],
            alternatives=alternatives,
            **kwargs
        ) for email in monitor.recipients
    ]


def schedule_zotero_transfers(monitor: Monitor):
    now = timezone.now()
    publication_keys = monitor.get_zotero_publication_keys()

    for api_key, path, collections in publication_keys:
        to_update = []
        existing = ZoteroTransfer.objects.filter(
            publication__in=monitor.publications,
            api_key=api_key,
            path=path,
        )

        for transfer in existing:
            if set(collections) - set(transfer.collection_keys):
                transfer.collection_keys = list(set(transfer.collection_keys) | set(collections))
                transfer.updated = now
                to_update.append(transfer)

        ZoteroTransfer.objects.bulk_update(to_update, fields=['collection_keys', 'updated'])

        to_create = monitor.publications.filter(zotero_transfers=None)

        ZoteroTransfer.objects.bulk_create([
            ZoteroTransfer(
                publication=publication,
                api_key=api_key,
                path=path,
                collection_keys=collections,
            ) for publication in to_create
        ])


def send_zotero_transfers(monitor: Monitor):
    transfers = ZoteroTransfer.objects.filter(publication__in=monitor.publications)

    new_transfers = transfers.filter(last_transferred=None)
    outdated_transfers = transfers.filter(last_transferred__lt=F('updated'))

    send_transfers(new_transfers)
    send_transfers(outdated_transfers, is_update=True)


def send_transfers(transfers: [ZoteroTransfer], is_update: bool = False):
    transfers_by_zotero_key = {
        get_zotero_object_key(transfer.publication): transfer
        for transfer in transfers
    }

    transfers_by_credentials = groupby(transfers, key=attrgetter('api_key', 'path'))

    for (api_key, path), group in transfers_by_credentials:
        data = get_zotero_data(group, is_update=is_update)

        for items in chunked(data, settings.ZOTERO_API_MAX_ITEMS):
            post_zotero_publication(items, api_key, path, transfers_by_zotero_key)


@app.task(ignore_result=True)
def send_publications_to_zotero(monitor: Union[int, Monitor]):
    if isinstance(monitor, int):
        monitor = Monitor.objects.get(pk=monitor)

    schedule_zotero_transfers(monitor)
    send_zotero_transfers(monitor)


def post_zotero_publication(data: List[dict], api_key: str, path: str, transfers: dict):
    url = build_zotero_api_url(path)
    headers = get_zotero_api_headers(api_key)
    session = TimeOutSession(settings.ZOTERO_API_TIMEOUT)

    ok, response = session.json('POST', url, json=data, headers=headers)

    now = timezone.now()

    if ok is None:
        capture_message(f'Zotero API failed with {response}', level='error')
    elif not ok:
        capture_message(f'Zotero API failed with status {response.status_code}', level='error')

    successful: dict = response.get('successful')
    successful_transfers = []

    for item in successful.values():
        key = item.get('key')
        version = item.get('version')
        transfer = transfers.get(key)

        if transfer:
            # the key might also belong to an attachment
            transfer.last_transferred = now
            transfer.version = version
            successful_transfers.append(transfer)

    ZoteroTransfer.objects.bulk_update(successful_transfers, fields=['last_transferred', 'version'])

    unchanged: dict = response.get('unchanged')
    failed: dict = response.get('failed')

    if failed:
        with push_scope() as scope:
            scope.set_extra('failed_items', [{**value, 'item': data[int(idx)]} for idx, value in failed.items()])
            capture_message(f'Failed to transfer Zotero items', level='error')

    if unchanged:
        # this shouldn't happen and indicates a mismatch of our data and the zotero data
        with push_scope() as scope:
            scope.set_extra('unchanged_items', [data[int(idx)] for idx in unchanged.keys()])
            capture_message(f'Zotero items have already been transferred', level='error')


@app.task(name='monitor.zotero')
def send_all_monitor_publications_to_zotero():
    monitors = Monitor.objects.filter(
        is_active=True,
        zotero_keys__len__gt=0,
    )

    for monitor in monitors:
        send_publications_to_zotero.delay(monitor.pk)


def send_monitor_publications(
    monitor: Monitor, *,
    now: datetime.datetime = None,
    exclude_sent: bool = True,
    **kwargs
) -> int:
    publications = list(monitor.get_publications(exclude_sent=exclude_sent))
    if not publications:
        return 0

    messages = make_monitor_publication_messages(monitor, publications, **kwargs)
    num_sent = get_mail_connection().send_messages(messages)

    if monitor.is_zotero:
        send_publications_to_zotero(monitor)

    monitor.last_sent = timezone.localtime(now)
    monitor.save(update_fields=['last_sent'])

    return num_sent
