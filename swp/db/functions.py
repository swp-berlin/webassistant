from django.db.models import F, Func, Value


class ArrayRemove(Func):
    function = 'array_remove'

    def __init__(self, array, element):
        if isinstance(array, str):
            array = F(array)

        if isinstance(element, str):
            element = Value(element)

        Func.__init__(self, array, element)
