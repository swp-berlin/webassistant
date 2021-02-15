import operator
from functools import reduce

from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from swp.models import Publication


def as_query(thinktank, filters):
    return models.Q(thinktank=thinktank) & reduce(operator.and_, filters, models.Q())


class ThinktankFilter(models.Model):
    """
    Filter query for think tank publication.
    """

    monitor = models.ForeignKey(
        'swp.Monitor',
        on_delete=models.CASCADE,
        related_name='thinktank_filters',
        verbose_name=_('monitor'),
    )

    thinktank = models.ForeignKey(
        'swp.Thinktank',
        on_delete=models.CASCADE,
        related_name='filters',
        verbose_name=_('think tank'),
    )

    publication_count = models.PositiveIntegerField(_('publication count'), default=0, editable=False)
    new_publication_count = models.PositiveIntegerField(_('new publication count'), default=0, editable=False)

    class Meta:
        verbose_name = _('think tank filter')
        verbose_name_plural = _('think tank filters')

    @cached_property
    def name(self) -> str:
        return self.thinktank.name

    @property
    def as_query(self):
        publication_filters = self.publication_filters.all()
        queries = [publication_filter.as_query for publication_filter in publication_filters]

        return as_query(self.thinktank, queries)

    def update_publication_count(self, *, last_sent=None, commit=True):
        last_sent = last_sent or self.monitor.last_sent
        publications = Publication.objects.active().filter(self.as_query)
        self.publication_count = publications.count()

        if last_sent:
            self.new_publication_count = publications.filter(last_access__gte=last_sent).count()
        else:
            self.new_publication_count = self.publication_count

        if commit:
            self.save(update_fields=['publication_count', 'new_publication_count'])
