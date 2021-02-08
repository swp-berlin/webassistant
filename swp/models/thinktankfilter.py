import operator
from functools import reduce

from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _


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

        return models.Q(thinktank=self.thinktank) & reduce(operator.and_, queries, models.Q())
