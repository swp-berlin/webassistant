from django.db import models
from django.utils.translation import gettext_lazy as _


class ThinktankFilter(models.Model):
    """
    Filter query for think tank publication.
    """

    monitor = models.ForeignKey(
        'swp.Monitor',
        on_delete=models.CASCADE,
        related_name='thinktank_filters',
        verbose_name=_('monitor'),
    )

    thinktank = models.ForeignKey(
        'swp.Thinktank',
        on_delete=models.CASCADE,
        related_name='filters',
        verbose_name=_('think tank'),
    )

    query = models.CharField(_('query'), max_length=1024)

    class Meta:
        verbose_name = _('think tank filter')
        verbose_name_plural = _('think tank filters')
