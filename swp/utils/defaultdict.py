from collections import defaultdict
from functools import partial


class NestedDefaultDict(defaultdict):

    def __init__(self, factory: callable, depth: int):
        for _ in range(depth):
            factory = partial(defaultdict, factory)

        defaultdict.__init__(self, factory)

    @classmethod
    def to_dict(cls, child):
        if isinstance(child, defaultdict):
            return {key: cls.to_dict(value) for key, value in child.items()}

        return child

    @property
    def dict(self):
        return self.to_dict(self)
