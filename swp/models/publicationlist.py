from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import (
    gettext_lazy as _,
    gettext_lazy as trans,  # use built in translations
)

from .abstract import LastModified


class PublicationList(LastModified):
    user = models.ForeignKey(
        verbose_name=trans('user'),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='publication_lists',
    )

    name = models.CharField(_('Name'), max_length=100)

    publications = models.ManyToManyField(
        verbose_name=_('Publications'),
        to='swp.Publication',
        through='swp.PublicationListEntry',
        blank=True,
    )

    class Meta:
        verbose_name = _('publication list')
        verbose_name_plural = _('publication lists')
        unique_together = [
            ('user', 'name'),
        ]

    def __str__(self):
        return self.name

    @cached_property
    def entry_count(self):
        return self.entries.count()

    @cached_property
    def last_updated(self):
        if last_entry_created := self.entries.aggregate(max=models.Max('created')).get('max'):
            return max(last_entry_created, self.last_modified)

        return self.last_modified


class PublicationListEntry(LastModified):
    publication_list = models.ForeignKey(
        verbose_name=_('publication list'),
        to=PublicationList,
        on_delete=models.CASCADE,
        related_name='entries',
    )

    publication = models.ForeignKey(
        verbose_name=_('publication list'),
        to='swp.Publication',
        on_delete=models.CASCADE,
        related_name='+',
    )

    created = models.DateTimeField(_('created'), default=timezone.now, editable=False)

    class Meta:
        verbose_name = _('publication list entry')
        verbose_name_plural = _('publication list entries')
        unique_together = [
            ('publication_list', 'publication'),
        ]
