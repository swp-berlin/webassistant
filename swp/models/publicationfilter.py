import operator
from functools import reduce

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Field
from django.db.models.lookups import IStartsWith, IEndsWith, IContains, PatternLookup, BuiltinLookup

from swp.models.choices import Comparator, FilterField
from swp.models.fields import ChoiceField


TEXT_FIELDS = [
    FilterField.TITLE,
    FilterField.SUBTITLE,
    FilterField.ABSTRACT,
]


class ArrayLookup(PatternLookup):
    def process_lhs(self, compiler, connection, lhs=None):
        lhs_sql, params = super(BuiltinLookup, self).process_lhs(compiler, connection, lhs)
        field_internal_type = self.lhs.output_field.get_internal_type()
        db_type = self.lhs.output_field.db_type(connection=connection)
        lhs_sql = connection.ops.field_cast_sql(db_type, field_internal_type) % lhs_sql
        cast = connection.ops.lookup_cast(super().lookup_name, field_internal_type) % 't'

        return 'EXISTS(SELECT * FROM UNNEST(%s) t WHERE %s' % (lhs_sql, cast), list(params)

    def process_rhs(self, qn, connection):
        rhs, params = super().process_rhs(qn, connection)

        return '%s)' % rhs, params


@ArrayField.register_lookup
class ArrayIStartsWith(ArrayLookup, IStartsWith):
    pass


@ArrayField.register_lookup
class ArrayIEndsWith(ArrayLookup, IEndsWith):
    pass


@ArrayField.register_lookup
class ArrayIStartswith(ArrayLookup, IContains):
    pass


def as_query(field, comparator, values):
    if field == FilterField.TEXT:
        return reduce(
            operator.or_,
            [as_query(text_field, comparator, values) for text_field in TEXT_FIELDS],
            models.Q(),
        )

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

    field = ChoiceField(_('field'), choices=FilterField.choices)
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
