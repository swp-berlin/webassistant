import datetime

from django.apps import apps
from django.db import DatabaseError, transaction
from django.utils.timezone import localtime

from swp.celery import app
from swp.models.publicationcount import PublicationCount


@app.task(name='publication-count.update', autoretry_for=[DatabaseError], retry_backoff=120)
def update_publication_count(model, pk, *, now=None, using=None):
    model = apps.get_model(model)

    assert issubclass(model, PublicationCount)

    now = localtime(now)
    deadline = now - datetime.timedelta(hours=1)

    with transaction.atomic(using):
        obj = model.objects.select_for_update(nowait=True).get(pk=pk)

        if obj.last_publication_count_update > deadline:
            return False

        return obj.update_publication_count(now=now)
