from django.contrib.postgres.fields import CICharField
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from .abstract import UpdateQuerySet, LastModified
from .user import User


class CanManageQuerySet(UpdateQuerySet):
    pool_ref = models.OuterRef('id')

    def annotate_can_manage(self, user: User):
        if user.has_pools:
            queryset = user.pools.through.objects.filter(user=user, pool=self.pool_ref)
            can_manage = models.Exists(queryset)
        else:
            can_manage = models.Value(True)

        return self.annotate(can_manage=can_manage)

    def can_manage(self, user: User):
        return self.annotate_can_manage(user).filter(can_manage=True)

    def can_research(self, user: User):
        if user.can_research_all_pools:
            return self.all()
        else:
            return self.can_manage(user)


class PoolQuerySet(CanManageQuerySet):
    pass


class Pool(LastModified):
    name = CICharField(_('name'), max_length=50, unique=True)

    objects = PoolQuerySet.as_manager()

    class Meta:
        verbose_name = _('pool')
        verbose_name_plural = _('pools')
        ordering = ['name']

    def __str__(self):
        return self.name

    @cached_property
    def thinktank_count(self) -> int:
        return self.thinktanks.count()
