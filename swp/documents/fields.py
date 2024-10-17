from typing import List

from django.contrib.postgres.fields import ArrayField
from django.db import models

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.documents import model_field_class_to_field_class
from elasticsearch_dsl import DenseVector

from swp.models.fields import CombinedISBNField, LongURLField, DenseVectorField

model_field_class_to_field_class[CombinedISBNField] = model_field_class_to_field_class[models.CharField]
model_field_class_to_field_class[LongURLField] = model_field_class_to_field_class[models.URLField]

ANALYZERS = {
    'ar': 'arabic',
    'bg': 'bulgarian',
    'bn': 'bengali',
    'ca': 'catalan',
    'ckb': 'sorani',
    'cs': 'czech',
    'da': 'danish',
    'de': 'german',
    'el': 'greek',
    'en': 'english',
    'es': 'spanish',
    'et': 'estonian',
    'eu': 'basque',
    'fa': 'persian',
    'fi': 'finnish',
    'fr': 'french',
    'ga': 'irish',
    'gl': 'galician',
    'hi': 'hindi',
    'hu': 'hungarian',
    'hy': 'armenian',
    'id': 'indonesian',
    'it': 'italian',
    'ja': 'cjk',
    'ko': 'cjk',
    'lt': 'lithuanian',
    'lv': 'latvian',
    'nl': 'dutch',
    'no': 'norwegian',
    'pt': 'portuguese',
    'ro': 'romanian',
    'ru': 'russian',
    'sv': 'swedish',
    'th': 'thai',
    'tr': 'turkish',
    'zh': 'cjk'
}


class TranslationField(fields.ObjectField):

    def __init__(self, attr=None, **kwargs):
        properties = {
            'default': fields.TextField(analyzer='default'),
        }

        for language, analyzer in ANALYZERS.items():
            properties[language] = fields.TextField(analyzer=analyzer)

        super(TranslationField, self).__init__(attr, properties=properties, **kwargs)

    def get_value_from_instance(self, instance, field_value_to_ignore=None):
        return {
            'default': super(fields.ObjectField, self).get_value_from_instance(
                instance=instance,
                field_value_to_ignore=field_value_to_ignore,
            ),
        }


def get_translation_fields(language, field_names):
    languages = [*ANALYZERS, 'default']

    if language in languages:
        languages.remove(language)
        languages.insert(0, language)

    return [f'{field}.{language}' for field in field_names for language in languages]


class FieldMixin:
    TRANSLATION_FIELDS: List[str] = []

    @classmethod
    def to_field(cls, field_name, model_field):
        if field_name in cls.TRANSLATION_FIELDS:
            return TranslationField(attr=field_name)

        if isinstance(model_field, DenseVectorField):
            return DenseVector(
                required=not model_field.null,
                dims=model_field.dims,
            )

        if isinstance(model_field, ArrayField):
            base_field = Document.to_field(field_name, model_field.base_field)

            return fields.ListField(base_field)

        return Document.to_field(field_name, model_field)
