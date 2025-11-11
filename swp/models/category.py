from django.contrib.postgres.fields import CICharField
from django.utils.translation import gettext_lazy as _

from swp.models.abstract import LastModified


class Category(LastModified):
    """
    A category to categorize publications.
    """

    name = CICharField(_('name'), max_length=50, unique=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name
