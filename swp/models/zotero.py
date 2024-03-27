from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex
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

    api_key = models.CharField(_('api key'), max_length=255, db_index=True)
    path = models.CharField(_('path'), max_length=255, db_index=True)
    key = ZoteroObjectKeyField(_('key'), null=True, blank=True)
    attachment_key = ZoteroObjectKeyField(_('attachment key'), null=True, blank=True)
    collection_keys = ArrayField(ZoteroObjectKeyField(), verbose_name=_('collection keys'), blank=True, default=list)

    version = models.IntegerField(_('version'), default=0, editable=False)

    created = models.DateTimeField(_('created'), default=timezone.now, editable=False)
    updated = models.DateTimeField(_('updated'), default=timezone.now, editable=False)
    last_transferred = models.DateTimeField(_('transferred'), null=True, blank=True)

    class Meta:
        verbose_name = _('zotero transfer')
        verbose_name_plural = _('zotero transfers')
        unique_together = [
            ('publication', 'api_key', 'path'),
        ]
        indexes = [
            GinIndex(fields=['collection_keys']),
            models.Index(models.Q(last_transferred__gte=models.F('updated')), name='transferred_after_updated_idx'),
        ]

    def __str__(self):
        return f'[{self.created}] {self.api_key}/{self.path} - {self.collection_keys}'
