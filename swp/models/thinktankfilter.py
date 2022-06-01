import operator

from functools import reduce

from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from .publicationcount import PublicationCount


def as_query(thinktank, filters):
    return reduce(operator.and_, filters, models.Q(thinktank=thinktank))


class ThinktankFilter(PublicationCount):
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

    def update_publication_count(self, *, last_sent=None, commit=True, now=None):
        return self.get_publication_counts(last_sent or self.monitor.last_sent, commit=commit, now=now)
