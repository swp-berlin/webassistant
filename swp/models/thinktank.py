from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Thinktank(models.Model):
    """
    Source of publications.
    """

    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    url = models.URLField(_('URL'), help_text=_('Link to homepage'))
    unique_field = models.CharField(_('unique field'), max_length=50)
    created = models.DateTimeField(_('created'), default=timezone.now, editable=False)

    class Meta:
        verbose_name = _('think tank')
        verbose_name_plural = _('think tanks')

    def __str__(self) -> str:
        return self.name
