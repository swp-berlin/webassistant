from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import Truncator
from django.utils.timezone import localdate
from django.utils.translation import gettext_lazy as _, ngettext

from swp.utils.text import when, spaced

from .constants import MAX_AUTHOR_LENGTH, MAX_TAG_LENGTH, MAX_TITLE_LENGTH
from .fields import CombinedISBNField, LongURLField, CharArrayField, DenseVectorField


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
        to='swp.Thinktank',
        on_delete=models.CASCADE,
        related_name='publications',
        verbose_name=_('think tank'),
    )

    scrapers = models.ManyToManyField(
        to='swp.Scraper',
        related_name='scraped_publications',
        verbose_name=_('scrapers'),
    )

    categories = models.ManyToManyField(
        to='swp.Category',
        related_name='publications',
        verbose_name=_('categories'),
        blank=True,
    )

    ris_type = models.CharField(_('reference type'), max_length=7, default='ICOMM')  # [TY]
    title = models.CharField(_('title'), max_length=MAX_TITLE_LENGTH)  # [T1]
    subtitle = models.CharField(_('subtitle'), max_length=255, blank=True)  # [T2]
    abstract = models.TextField(_('abstract'), blank=True)  # [AB]
    authors = CharArrayField(max_length=MAX_AUTHOR_LENGTH, blank=True, null=True, verbose_name=_('authors'))  # [AU]
    publication_date = models.CharField(_('publication date'), max_length=255, blank=True, default='')  # [PY]
    publication_date_clean = models.DateField(_('publication date (clean)'), blank=True)
    last_access = models.DateTimeField(_('last access'), default=timezone.now, editable=False)  # [Y2]
    url = LongURLField(_('URL'))  # [UR]
    pdf_url = LongURLField(_('PDF URL'), blank=True)  # [L1]
    pdf_pages = models.PositiveIntegerField(_('number of pages'), default=0)  # [EP]
    doi = models.CharField(_('DOI'), max_length=255, blank=True)  # [DO]
    isbn = CombinedISBNField(_('ISBN/ISSN'), blank=True)  # [SN]
    tags = CharArrayField(max_length=MAX_TAG_LENGTH, blank=True, default=list, verbose_name=_('tags'))  # [KW]
    created = models.DateTimeField(_('created'), default=timezone.now, editable=False)
    hash = models.CharField(_('hash'), max_length=32, blank=True, null=True)
    embedding = DenseVectorField(_('embedding'), dims=settings.EMBEDDING_VECTOR_DIMS, null=True, editable=False)

    objects = PublicationQuerySet.as_manager()

    class Meta:
        verbose_name = _('publication')
        verbose_name_plural = _('publications')
        permissions = [
            ('can_research', 'Can use research interface'),
        ]

    def __str__(self) -> str:
        return self.title_label

    @property
    def title_label(self):
        return spaced(self.title) or f'{self.pk}'

    @property
    def authors_label(self):
        return joined(self.authors or [], '; ')

    @property
    def abstract_label(self):
        if abstract := spaced(self.abstract):
            return Truncator(abstract).words(120)

    @property
    def tags_label(self):
        return joined(self.tags or [], ', ')

    @property
    def pdf_pages_label(self):
        return ngettext('%d page', '%d pages', self.pdf_pages) % self.pdf_pages

    @property
    def source(self):
        return self.url or self.pdf_url

    def save(self, **kwargs):
        if self.publication_date_clean is None:
            self.publication_date_clean = localdate(self.created)

        return super().save(**kwargs)


def joined(values, delimiter, default='–'):
    return delimiter.join(when(spaced(value) for value in values)) or default
