from __future__ import annotations

import datetime
import functools
from typing import Any, Mapping, Sequence, TYPE_CHECKING

from django import forms
from django.contrib.postgres.forms import SimpleArrayField
from django.db import models
from django.utils import timezone
from django.utils.text import Truncator
from django.utils.translation import gettext_lazy as _

from swp.models import Publication
if TYPE_CHECKING:
    from swp.models import Thinktank


class ScrapedPublicationForm(forms.ModelForm):

    title = forms.CharField(label=_('title'))
    subtitle = forms.CharField(label=_('subtitle'), required=False)
    authors = SimpleArrayField(forms.CharField(required=False), label=_('authors'), required=False)
    pdf_path = forms.CharField(label=_('PDF path'), required=False)
    text_content = forms.CharField(label=_('Text Content'), required=False)

    class Meta:
        model = Publication
        exclude = [
            'thinktank',
            'created',
            'last_access',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in ['scrapers', 'ris_type', 'pdf_pages']:
            self.fields[field].required = False

    @classmethod
    @functools.lru_cache(8)
    def get_model_field(cls, field) -> models.Field:
        return cls.Meta.model._meta.get_field(field)

    @classmethod
    def truncate(cls, value: str, max_length: int) -> str:
        return Truncator(value).chars(max_length)

    def truncated_field(self, field: str) -> str:
        value = self.cleaned_data.get(field)
        field = self.get_model_field(field)

        return self.truncate(value, field.max_length)

    def clean_title(self) -> str:
        return self.truncated_field('title')

    def clean_subtitle(self) -> str:
        return self.truncated_field('subtitle')

    def clean_authors(self) -> Sequence[str]:
        items = self.cleaned_data.get('authors') or []
        field = self.get_model_field('authors')
        clean = functools.partial(self.truncate, max_length=field.base_field.max_length)

        return [clean(author) for author in items]

    def clean(self) -> Mapping[str, Any]:
        super().clean()

        ris_type = self.cleaned_data.get('ris_type')
        if not ris_type:
            pdf_url = self.cleaned_data.get('pdf_url')
            self.cleaned_data['ris_type'] = 'UNPB' if pdf_url else 'ICOMM'

        return self.cleaned_data

    def save(self, commit: bool = True, *, thinktank: Thinktank = None, now: datetime.datetime = None) -> Publication:
        if thinktank is not None:
            self.instance.thinktank = thinktank

        self.instance.created = self.instance.last_access = timezone.localtime(now)

        for embedding_field in ['pdf_path', 'text_content']:
            setattr(self.instance, embedding_field, self.cleaned_data.get(embedding_field))

        return super().save(commit=commit)
