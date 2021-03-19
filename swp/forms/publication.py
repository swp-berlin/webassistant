import datetime
import functools
from typing import Any, Mapping, Sequence

from django.db import models
from django.forms import ModelForm
from django.utils import timezone
from django.utils.text import Truncator

from swp.models import Publication


class ScrapedPublicationForm(ModelForm):

    class Meta:
        model = Publication
        fields = '__all__'

    def __init__(self, *args, now: datetime.datetime = None, **kwargs):
        super().__init__(*args, **kwargs)

        self.now = timezone.localtime(now)
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

    def clean_last_access(self) -> datetime.datetime:
        return self.cleaned_data.get('last_access') or self.now

    def clean_created(self) -> datetime.datetime:
        return self.cleaned_data.get('created') or self.now

    def clean(self) -> Mapping[str, Any]:
        super().clean()

        ris_type = self.cleaned_data.get('ris_type')
        if not ris_type:
            pdf_url = self.cleaned_data.get('pdf_url')
            self.cleaned_data['ris_type'] = 'UNPB' if pdf_url else 'ICOMM'

        return self.cleaned_data
