from django.db.models import CharField


class ChoiceField(CharField):

    def __init__(self, verbose_name=None, *, choices, **kwargs):
        max_length = max(map(len, dict(choices)))
        (default, label), *others = choices

        kwargs.setdefault('max_length', max_length)
        kwargs.setdefault('default', default)
        kwargs.setdefault('db_index', True)

        super(ChoiceField, self).__init__(verbose_name=verbose_name, choices=choices, **kwargs)
