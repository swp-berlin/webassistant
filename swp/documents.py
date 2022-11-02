from django.contrib.postgres.fields import ArrayField
from django.db import models

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.documents import model_field_class_to_field_class
from django_elasticsearch_dsl.registries import registry

from swp.models import Publication
from swp.models.fields import CombinedISBNField, LongURLField

model_field_class_to_field_class[CombinedISBNField] = model_field_class_to_field_class[models.CharField]
model_field_class_to_field_class[LongURLField] = model_field_class_to_field_class[models.URLField]


@registry.register_document
class PublicationDocument(Document):

    class Index:
        name = 'publications'

    class Django:
        model = Publication
        fields = [
            'ris_type',
            'title',
            'subtitle',
            'abstract',
            'authors',
            'publication_date',
            'last_access',
            'url',
            'pdf_url',
            'pdf_pages',
            'doi',
            'isbn',
            'tags',
            'created',
            'hash',
        ]

    @classmethod
    def to_field(cls, field_name, model_field):
        if isinstance(model_field, ArrayField):
            base_field = Document.to_field(field_name, model_field.base_field)

            return fields.ListField(base_field)

        return Document.to_field(field_name, model_field)
