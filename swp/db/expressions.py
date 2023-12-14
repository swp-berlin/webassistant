from django.db.models import BooleanField, DurationField, ExpressionWrapper, Func, Q


class MakeInterval(Func):
    function = 'make_interval'
    template = '%(function)s(%(key)s => %(expressions)s)'
    output_field = DurationField(default=None)

    def __init__(self, **kwargs):
        if len(kwargs) > 1:
            raise NotImplementedError('Currently, there is just one keyword supported.')

        [(key, value)] = kwargs.items()

        super(MakeInterval, self).__init__(value, output_field=self.output_field, key=key)


class QueryExpression(ExpressionWrapper):

    def __init__(self, *args, **kwargs):
        super(QueryExpression, self).__init__(Q(*args, **kwargs), BooleanField(default=False))
