from django.db import models
from django.utils.translation import gettext_lazy as _


class ScraperType(models.Model):
    """
    Configuration for scraping of web sites.
    """

    name = models.CharField(_('name'), max_length=100, unique=True)
    config = models.JSONField(_('config'), default=dict)

    class Meta:
        verbose_name = _('scraper type')
        verbose_name_plural = _('scraper types')

    def __str__(self) -> str:
        return self.name
