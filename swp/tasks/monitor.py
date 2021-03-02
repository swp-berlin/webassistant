import datetime
from typing import Optional

from celery import group
from celery.result import AsyncResult
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.utils import timezone

from cosmogo.utils.mail import render_mail

from swp.celery import app
from swp.models import Monitor
from swp.utils.ris import RIS_MEDIA_TYPE


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
def monitor_new_publications(monitor_id: int, **kwargs) -> Optional[AsyncResult]:
    """ Dispatch new monitor publications to all recipients. """
    with transaction.atomic(using=kwargs.get('using')):
        monitor = Monitor.objects.get_for_update(pk=monitor_id)
        if not monitor.is_active:
            return None

        monitor.update_publication_count()
        if not monitor.new_publication_count:
            return None

        if not monitor.recipients:
            return None

        job = group([
            send_monitor_publications_mail.si(
                monitor.pk,
                email,
                exclude_sent=True,
                **kwargs
            ) for email in monitor.recipients
        ], link=update_monitor_sent.si(monitor_id))

        return job()


@app.task(name='monitor.update-sent')
def update_monitor_sent(monitor_id: int, now: datetime.datetime = None, **kwargs):
    now = timezone.localtime(now)
    with transaction.atomic(using=kwargs.get('using')):
        # We update the timestamp here instead of each mail task,
        # since otherwise we would not get "new" publications after
        # the first such call.
        #
        # As a result ``last_sent`` does not imply success.
        Monitor.objects.select_for_update().filter(pk=monitor_id).update(last_sent=now)


@app.task(name='monitor.send-publications-mail')
def send_monitor_publications_mail(monitor_id: int, email: str, *, exclude_sent: bool = True, **kwargs) -> int:
    """ Send email with new publications for monitor to single recipient. """
    with transaction.atomic(using=kwargs.get('using')):
        monitor = Monitor.objects.get(pk=monitor_id)
        if not monitor.is_active:
            return 0

        publications = list(monitor.get_publications(exclude_sent=exclude_sent))
        publication_count = len(publications)
        if not publication_count:
            return 0

        context = {
            'monitor': monitor,
            'publication_count': publication_count,
        }

        subject, message, html_message = render_mail('monitor-publications', context=context)

        mail = EmailMultiAlternatives(
            subject=subject,
            body=message,
            to=[email],
        )
        if html_message:
            mail.attach_alternative(html_message, 'text/html')

        ris_file = monitor.generate_ris_file(exclude_sent=exclude_sent)
        mail.attach(ris_file.name, ris_file.file.getvalue(), RIS_MEDIA_TYPE)

        return mail.send()
