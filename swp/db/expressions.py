from django.db import models


class MakeInterval(models.Func):
    function = 'make_interval'
    template = '%(function)s(%(key)s => %(expressions)s)'
    output_field = models.DurationField(default=None)

    def __init__(self, **kwargs):
        if len(kwargs) > 1:
            raise NotImplementedError('Currently there is just one keyword supported.')

        [(key, value)] = kwargs.items()

        super(MakeInterval, self).__init__(value, output_field=self.output_field, key=key)
