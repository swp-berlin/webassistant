import datetime

from typing import Tuple

from django.db import models
from django.utils.timezone import localtime
from django.utils.translation import gettext_lazy as _

from .publication import Publication


class PublicationCount(models.Model):
    publication_count = models.PositiveIntegerField(_('publication count'), default=0, editable=False)
    new_publication_count = models.PositiveIntegerField(_('new publication count'), default=0, editable=False)
    last_publication_count_update = models.DateTimeField(
        verbose_name=_('last publication count update'),
        null=True,
        blank=True,
        editable=False,
    )

    class Meta:
        abstract = True

    as_query: models.Q

    def update_publication_count(self, *, commit: bool = True, now: datetime.datetime = None) -> Tuple[int, int]:
        raise NotImplementedError

    def get_publication_counts(self, last_sent, *, commit: bool, now: datetime.datetime) -> Tuple[int, int]:
        publications = Publication.objects.active().filter(self.as_query)

        self.publication_count = publications.count()

        if last_sent:
            self.new_publication_count = publications.filter(last_access__gte=last_sent).count()
        else:
            self.new_publication_count = self.publication_count

        self.last_publication_count_update = localtime(now)

        if commit:
            self.save(update_fields=['publication_count', 'new_publication_count', 'last_publication_count_update'])

        return self.publication_count, self.new_publication_count
