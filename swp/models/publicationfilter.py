import operator
from functools import reduce

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from swp.models.choices import Comparator, DataResolverKey
from swp.models.fields import ChoiceField


def as_query(field, comparator, values):
    key = f'{field}__{PublicationFilter.FILTERS[comparator]}'

    return reduce(
        operator.or_,
        [models.Q(**{key: value}) for value in values],
        models.Q(),
    )


class PublicationFilter(models.Model):
    FILTERS = {
        Comparator.CONTAINS: 'icontains',
        Comparator.STARTS_WITH: 'istartswith',
        Comparator.ENDS_WITH: 'iendswith'
    }

    thinktank_filter = models.ForeignKey(
        'swp.ThinktankFilter',
        on_delete=models.CASCADE,
        related_name='publication_filters',
        verbose_name=_('think tank filter'),

    )

    field = ChoiceField(_('field'), choices=DataResolverKey.choices)
    comparator = ChoiceField(_('comparator'), choices=Comparator.choices)
    values = ArrayField(
        verbose_name=_('values'),
        base_field=models.CharField(max_length=255),
    )

    class Meta:
        verbose_name = _('publication filter')
        verbose_name_plural = _('publication filters')

    def __str__(self):
        return f'{self.field} {self.comparator} "{self.values}"'

    @property
    def as_query(self):
        return as_query(self.field, self.comparator, self.values)
