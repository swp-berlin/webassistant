from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from swp.models.fields import ZoteroObjectKeyField


class ZoteroTransfer(models.Model):
    publication = models.ForeignKey(
        to='swp.Publication',
        verbose_name=_('publication'),
        related_name='zotero_transfers',
        on_delete=models.CASCADE,
    )

    api_key = models.CharField(_('api key'), max_length=255)
    path = models.CharField(_('path'), max_length=255)
    collection_keys = ArrayField(
        ZoteroObjectKeyField(),
        verbose_name=_('collection keys'),
        blank=True,
        default=list,
    )

    version = models.IntegerField(_('version'), default=0, editable=False)

    created = models.DateTimeField(_('created'), default=timezone.now, editable=False)
    updated = models.DateTimeField(_('updated'), default=timezone.now, editable=False)
    last_transferred = models.DateTimeField(_('transferred'), null=True, blank=True)

    class Meta:
        unique_together = ['publication', 'api_key', 'path']
        verbose_name = _('zotero transfer')
        verbose_name_plural = _('zotero transfers')

    def __str__(self):
        return f'[{self.created}] {self.api_key}/{self.path} - {self.collection_keys}'
