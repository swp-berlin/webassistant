from django.contrib.postgres.fields import CICharField
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from .abstract import LastModified


class Pool(LastModified):
    name = CICharField(_('name'), max_length=50, unique=True)

    class Meta:
        verbose_name = _('pool')
        verbose_name_plural = _('pools')
        ordering = ['name']

    def __str__(self):
        return self.name

    @cached_property
    def thinktank_count(self) -> int:
        return self.thinktanks.count()
