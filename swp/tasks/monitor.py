import datetime
from typing import Iterable, List, Optional

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection as get_mail_connection
from django.db import transaction
from django.utils import timezone

from sentry_sdk import capture_message
from cosmogo.utils.mail import render_mail
from cosmogo.utils.requests import TimeOutSession

from swp.celery import app
from swp.models import Monitor, Publication
from swp.utils.ris import generate_ris_attachment
from swp.utils.zotero import get_zotero_data, build_zotero_api_url, get_zotero_api_headers


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


def send_monitor_publications_to_zotero(monitor: Monitor, publications: Iterable[Publication]):
    data = get_zotero_data(publications)
    for key in monitor.zotero_keys:
        api_key, sep, path = key.partition('/')
        path = f'{sep}{path}'

        n = settings.ZOTERO_API_MAX_ITEMS
        for items in [data[i:i + n] for i in range(0, len(data), n)]:
            post_zotero_publication.delay(
                items,
                api_key,
                path,
            )


@app.task(ignore_result=True)
def post_zotero_publication(data: List[dict], api_key: str, path: str):
    url = build_zotero_api_url(path)
    headers = get_zotero_api_headers(api_key)
    session = TimeOutSession(settings.ZOTERO_API_TIMEOUT)

    ok, response = session.json('POST', url, json=data, headers=headers)
    if ok is None:
        capture_message(f'Zotero API failed with {response}', level='error')
    elif not ok:
        capture_message(f'Zotero API failed with status {response.status_code}', level='error')
    elif response:
        failure = response.get('failure')
        if failure:
            capture_message(f'Zotero API failed with {failure}')

    return response


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
        send_monitor_publications_to_zotero(monitor, publications)

    monitor.last_sent = timezone.localtime(now)
    monitor.save(update_fields=['last_sent'])

    return num_sent
