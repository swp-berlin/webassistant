from __future__ import annotations

import datetime
from typing import Iterable, TYPE_CHECKING

from django.db import models
from django.template.defaultfilters import truncatechars
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

from .fields import LongURLField
if TYPE_CHECKING:
    from .thinktank import Thinktank


class PublicationQuerySet(models.QuerySet):

    def active(self) -> PublicationQuerySet:
        return self.filter(thinktank__is_active=True)

    def inactive(self) -> PublicationQuerySet:
        return self.filter(thinktank__is_active=False)


class Publication(models.Model):
    """
    Single published article.
    """

    thinktank = models.ForeignKey(
        'swp.Thinktank',
        on_delete=models.CASCADE,
        related_name='publications',
        verbose_name=_('think tank'),
    )

    scrapers = models.ManyToManyField(
        'swp.Scraper',
        related_name='scraped_publications',
        verbose_name=_('scrapers'),
    )

    ris_type = models.CharField(_('reference type'), max_length=7, default='ICOMM')  # [TY]
    title = models.CharField(_('title'), max_length=255)  # [T1]
    subtitle = models.CharField(_('subtitle'), max_length=255, blank=True)  # [T2]
    abstract = models.TextField(_('abstract'), blank=True)  # [AB]
    authors = ArrayField(models.CharField(max_length=255), blank=True, null=True, verbose_name=_('authors'))  # [AU]
    publication_date = models.CharField(_('publication date'), max_length=255, blank=True, default='')  # [PY]
    last_access = models.DateTimeField(_('last access'), default=timezone.now, editable=False)  # [Y2]
    url = LongURLField(_('URL'))  # [UR]
    pdf_url = LongURLField(_('PDF URL'), blank=True)  # [L1]
    pdf_pages = models.PositiveIntegerField(_('number of pages'), default=0)  # [EP]
    tags = ArrayField(models.CharField(max_length=32), blank=True, null=True, verbose_name=_('tags'))  # [KW]
    created = models.DateTimeField(_('created'), default=timezone.now, editable=False)

    objects = PublicationQuerySet.as_manager()

    class Meta:
        verbose_name = _('publication')
        verbose_name_plural = _('publications')

    def __str__(self) -> str:
        return self.title or f'{self.pk}'

    @classmethod
    def normalize_title(cls, value: str) -> str:
        value = str.strip(value or '')
        max_length = cls._meta.get_field('title').max_length

        return truncatechars(value, max_length) if value else ''

    @classmethod
    def normalize_subtitle(cls, value: str) -> str:
        value = str.strip(value or '')
        max_length = cls._meta.get_field('subtitle').max_length

        return truncatechars(value, max_length) if value else ''

    @classmethod
    def normalize_author(cls, value: str) -> str:
        value = str.strip(value or '')
        max_length = cls._meta.get_field('authors').base_field.max_length

        return truncatechars(value, max_length) if value else ''

    @classmethod
    def create(
        cls,
        thinktank: Thinktank, *,
        title: str,
        subtitle: str = '',
        authors: Iterable[str] = (),
        now: datetime.datetime = None,
        **fields
    ) -> Publication:
        fields['title'] = cls.normalize_title(title)
        fields['subtitle'] = cls.normalize_subtitle(subtitle)
        fields['authors'] = [cls.normalize_author(author) for author in authors]

        fields.setdefault('ris_type', 'UNPB' if 'pdf_url' in fields else 'ICOMM')

        now = timezone.localtime(now)
        fields.setdefault('created', now)
        fields.setdefault('last_access', now)

        return cls(thinktank=thinktank, **fields)
