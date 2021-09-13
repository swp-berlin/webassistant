from django.contrib.postgres.fields import ArrayField
from django.db.models.lookups import IStartsWith, IEndsWith, IContains, PatternLookup, BuiltinLookup


class ArrayLookup(PatternLookup):
    def as_sql(self, compiler, connection):
        sql, params = super().as_sql(compiler, connection)
        return 'EXISTS(%s)' % sql, params

    def process_lhs(self, compiler, connection, lhs=None):
        lhs_sql, params = super(BuiltinLookup, self).process_lhs(compiler, connection, lhs)
        field_internal_type = self.lhs.output_field.get_internal_type()
        db_type = self.lhs.output_field.db_type(connection=connection)
        lhs_sql = connection.ops.field_cast_sql(db_type, field_internal_type) % lhs_sql

        return 'SELECT 1 FROM UNNEST(%s) t WHERE UPPER(t)' % lhs_sql, list(params)


@ArrayField.register_lookup
class ArrayIStartsWith(ArrayLookup, IStartsWith):
    pass


@ArrayField.register_lookup
class ArrayIEndsWith(ArrayLookup, IEndsWith):
    pass


@ArrayField.register_lookup
class ArrayIStartswith(ArrayLookup, IContains):
    pass
