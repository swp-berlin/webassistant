from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from swp.models.abstract import LastModified
from swp.utils.translation import trans


class AuthToken(LastModified):
    user = models.OneToOneField(
        verbose_name=trans('user'),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='auth_token',
    )
    key = models.UUIDField(_('key'), editable=False, unique=True, default=uuid4)
    expires = models.DateTimeField(_('expires'), null=True, blank=True)

    class Meta:
        verbose_name = _('auth token')
        verbose_name_plural = _('auth tokens')

    def __str__(self):
        return f'{self.key}'
