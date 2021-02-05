import operator
from functools import reduce

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

from .publication import Publication
from .abstract import ActivatableModel
from .choices import Interval


class Monitor(ActivatableModel):
    """
    Monitoring profile for a topic of interest.
    """

    name = models.CharField(_('name'), max_length=100)
    recipients = ArrayField(models.EmailField(), verbose_name=_('recipients'))
    interval = models.PositiveIntegerField(_('interval'), choices=Interval.choices, default=Interval.DAILY)
    last_sent = models.DateTimeField(_('last sent'), blank=True, null=True)
    created = models.DateTimeField(_('created'), default=timezone.now, editable=False)

    class Meta(ActivatableModel.Meta):
        verbose_name = _('monitor')
        verbose_name_plural = _('monitors')

    def __str__(self) -> str:
        return self.name

    @property
    def as_query(self):
        thinktank_filters = self.thinktank_filters.all()
        queries = [thinktank_filter.as_query for thinktank_filter in thinktank_filters]

        return reduce(operator.or_, queries, models.Q())

    @property
    def recipient_count(self):
        return len(self.recipients)

    @property
    def publications(self):
        return Publication.objects.filter(self.as_query)

    @property
    def publication_count(self):
        return self.publications.count()

    @property
    def new_publication_count(self):
        publications = self.publications

        if self.last_sent:
            publications = publications.filter(created__gt=self.last_sent)

        return publications.count()
