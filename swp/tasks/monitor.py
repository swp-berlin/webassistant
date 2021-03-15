import datetime
from typing import Iterable, Optional

from django.core.mail import EmailMultiAlternatives, get_connection as get_mail_connection
from django.db import transaction
from django.utils import timezone

from cosmogo.utils.mail import render_mail

from swp.celery import app
from swp.models import Monitor, Publication
from swp.utils.ris import generate_ris_attachment


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

    monitor.last_sent = timezone.localtime(now)
    monitor.save(update_fields=['last_sent'])

    return num_sent
