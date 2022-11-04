from typing import List

from django.contrib.postgres.fields import ArrayField
from django.db import models

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.documents import model_field_class_to_field_class

from swp.models.fields import CombinedISBNField, LongURLField

model_field_class_to_field_class[CombinedISBNField] = model_field_class_to_field_class[models.CharField]
model_field_class_to_field_class[LongURLField] = model_field_class_to_field_class[models.URLField]

ANALYZERS = {
    'de': 'german',
    'en': 'english',
    'es': 'spanish',
    'fr': 'french',
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


class FieldMixin:
    TRANSLATION_FIELDS: List[str] = []

    @classmethod
    def to_field(cls, field_name, model_field):
        if field_name in cls.TRANSLATION_FIELDS:
            return TranslationField(attr=field_name)

        if isinstance(model_field, ArrayField):
            base_field = Document.to_field(field_name, model_field.base_field)

            return fields.ListField(base_field)

        return Document.to_field(field_name, model_field)
