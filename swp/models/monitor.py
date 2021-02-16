import operator
from functools import reduce

from django.db import models
from django.db.models import Count
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
    description = models.TextField(_('description'), blank=True)
    recipients = ArrayField(models.EmailField(), blank=True, verbose_name=_('recipients'))
    interval = models.PositiveIntegerField(_('interval'), choices=Interval.choices, default=Interval.DAILY)
    last_sent = models.DateTimeField(_('last sent'), blank=True, null=True)
    created = models.DateTimeField(_('created'), default=timezone.now, editable=False)

    publication_count = models.PositiveIntegerField(_('publication count'), default=0, editable=False)
    new_publication_count = models.PositiveIntegerField(_('new publication count'), default=0, editable=False)

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
        return Publication.objects.active().filter(self.as_query)

    def update_publication_count(self, commit=True):
        publications = Publication.objects.active().filter(self.as_query)

        self.publication_count = publications.count()

        if self.last_sent:
            self.new_publication_count = publications.filter(last_access__gte=self.last_sent).count()
        else:
            self.new_publication_count = self.publication_count

        for filter in self.thinktank_filters.all():
            filter.update_publication_count(last_sent=self.last_sent)

        if commit:
            self.save(update_fields=['publication_count', 'new_publication_count'])
