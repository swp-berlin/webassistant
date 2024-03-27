import datetime
from typing import Iterable, List, Optional, Union, Mapping, Any

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection as get_mail_connection
from django.db import transaction
from django.db.models import F, Q
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from sentry_sdk import capture_message, push_scope
from swp.utils.mail import render_mail

from swp.celery import app
from swp.models import Monitor, Publication
from swp.models.zotero import ZoteroTransfer
from swp.utils.requests import TimeOutSession
from swp.utils.ris import generate_ris_attachment
from swp.utils.zotero import (
    build_zotero_api_url,
    get_zotero_api_headers,
    get_zotero_attachment_data,
    get_zotero_publication_data,
)


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
def monitor_new_publications(monitor_id: int, now: datetime.datetime = None, *, using=None, **kwargs) -> Optional[int]:
    """ Dispatch new monitor publications to all recipients. """
    with transaction.atomic(using=using):
        monitor = Monitor.objects.using(using).get_for_update(pk=monitor_id)

        if not monitor.is_active:
            return None

        monitor.update_publication_count(now=now)

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
        'publications': publications,
        'last_sent': monitor.last_sent or monitor.created,
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

    publications = monitor.get_publications()

    for api_key, path, collections in publication_keys:
        to_update = []

        publication_ids = {p.pk for p in publications}

        existing = ZoteroTransfer.objects.filter(
            publication__in=monitor.publications,
            api_key=api_key,
            path=path,
        )

        for transfer in existing:
            publication_ids.remove(transfer.publication_id)
            if set(collections) - set(transfer.collection_keys):
                transfer.collection_keys = list(set(transfer.collection_keys) | set(collections))
                transfer.updated = now
                to_update.append(transfer)

        ZoteroTransfer.objects.bulk_update(to_update, fields=['collection_keys', 'updated'])

        ZoteroTransfer.objects.bulk_create([
            ZoteroTransfer(
                publication_id=publication_id,
                api_key=api_key,
                path=path,
                collection_keys=collections,
            ) for publication_id in publication_ids
        ])


def send_zotero_transfers(monitor: Monitor):
    transfers = ZoteroTransfer.objects.filter(
        Q(last_transferred=None) | Q(last_transferred__lt=F('updated')),
        publication__in=monitor.publications
    )

    for transfer in transfers:
        transfer_publication.delay(transfer.pk, transfer.updated)


@app.task(ignore_result=True)
def send_publications_to_zotero(monitor: Union[int, Monitor]):
    if isinstance(monitor, int):
        monitor = Monitor.objects.get(pk=monitor)

    schedule_zotero_transfers(monitor)
    send_zotero_transfers(monitor)


def post_zotero_items(data: List[dict], api_key: str, path: str) -> Optional[dict]:
    url = build_zotero_api_url(path)
    headers = get_zotero_api_headers(api_key)
    session = TimeOutSession(settings.ZOTERO_API_TIMEOUT)

    ok, response = session.json('POST', url, json=data, headers=headers)

    if ok is None:
        capture_message(f'Zotero API failed with {response}', level='error')
        return None
    elif not ok:
        capture_message(f'Zotero API failed with status {response.status_code}', level='error')
        return None

    return response


@app.task(name='transfer_publication')
def transfer_publication(transfer: Union[ZoteroTransfer, int], scheduled: Union[str, datetime.datetime]):
    with transaction.atomic():
        if isinstance(transfer, int):
            transfer = ZoteroTransfer.objects.select_for_update().get(pk=transfer)

        if isinstance(scheduled, str):
            scheduled = parse_datetime(scheduled)

        if transfer.updated > scheduled:
            # transfer has been updated in the meantime
            # another task will transfer this
            return

        post_transfer(transfer)


def post_transfer(transfer: ZoteroTransfer):
    item = get_zotero_publication_data(transfer)

    obj = post_zotero_item(item, transfer.api_key, transfer.path)

    if not obj:
        return

    object_key = obj.get('key')
    version = obj.get('version')

    transfer.key = object_key
    transfer.version = version

    if transfer.publication.pdf_url and not transfer.attachment_key:
        # attachment has not been transferred yet for this publication
        post_transfer_attachment(transfer)

    transfer.last_transferred = timezone.now()

    transfer.save(update_fields=['key', 'attachment_key', 'version', 'last_transferred'])


def post_transfer_attachment(transfer: ZoteroTransfer):
    item = get_zotero_attachment_data(transfer)

    obj = post_zotero_item(item, transfer.api_key, transfer.path)

    if not obj:
        return

    object_key = obj.get('key')

    transfer.attachment_key = object_key


def post_zotero_item(item: Mapping[str, Any], api_key: str, path: str):
    url = build_zotero_api_url(path)

    headers = get_zotero_api_headers(api_key)
    session = TimeOutSession(settings.ZOTERO_API_TIMEOUT)

    ok, response = session.json('POST', url, json=[item], headers=headers)

    with push_scope() as scope:
        scope.set_extra('item', item)
        scope.set_extra('url', url)
        scope.set_extra('response', response)

        if ok is None:
            capture_message(f'Zotero API failed with {response}', level='error')
            return None
        elif not ok:
            capture_message(f'Zotero API failed with status {response.status_code}', level='error')
            return None

        successful: dict = response.get('successful')

        if not successful:
            capture_message(f'Zotero API failed to transfer items', level='error')
            return None

    return successful.get('0')


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
