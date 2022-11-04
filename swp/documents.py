from django.contrib.postgres.fields import ArrayField
from django.db import models

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.indices import Index
from django_elasticsearch_dsl.documents import model_field_class_to_field_class

from elasticsearch.client.ingest import IngestClient

from swp.models import Publication
from swp.models.fields import CombinedISBNField, LongURLField

model_field_class_to_field_class[CombinedISBNField] = model_field_class_to_field_class[models.CharField]
model_field_class_to_field_class[LongURLField] = model_field_class_to_field_class[models.URLField]

ANALYZERS = {
    'de': 'german',
    'en': 'english',
    'es': 'spanish',
    'fr': 'french',
}

LANGUAGES = [*ANALYZERS]


class TranslationField(fields.ObjectField):

    def __init__(self):
        properties = {
            'default': fields.TextField(analyzer='default'),
        }

        for language, analyzer in ANALYZERS.items():
            properties[language] = fields.TextField(analyzer=analyzer)

        super(TranslationField, self).__init__(properties=properties)

    def get_value_from_instance(self, instance, field_value_to_ignore=None):
        return {
            'default': super(fields.ObjectField, self).get_value_from_instance(
                instance=instance,
                field_value_to_ignore=field_value_to_ignore,
            ),
        }


class PublicationIndex(Index):

    def create(self, using=None, **kwargs):
        result = Index.create(self, using=using, **kwargs)

        self.add_language_detection('title', 'subtitle', 'abstract')

        return result

    def put_ingest_pipeline(self, **kwargs):
        return IngestClient(self.connection).put_pipeline(**kwargs)

    def add_language_detection(self, *field_names, target_field='_language'):
        languages = ', '.join(f"'{language}'" for language in LANGUAGES)

        return self.put_ingest_pipeline(
            id='language-detection',
            body={
                'processors': [
                    {
                        'inference': {
                            'model_id': 'lang_ident_model_1',
                            'inference_config': {
                                'classification': {
                                    'num_top_classes': 0,
                                },
                            },
                            'field_map': {f'{field}.default': 'text' for field in field_names},
                            'target_field': target_field,
                        },
                    },
                    {
                        'script': {
                            'lang': 'painless',
                            'source': f"""
                                ctx.{target_field}.supported = ([{languages}].contains(
                                    ctx.{target_field}.predicted_value)
                                )
                            """,
                        },
                    },
                    *self.get_field_pipeline(field_names, target_field),
                ],
            },
        )

    @staticmethod
    def get_field_pipeline(field_names, target_field):
        for field in field_names:
            context = {'field': field, 'target_field': target_field}

            yield {
                'set': {
                    'if': f'ctx.{target_field}.supported',
                    'field': '%(field)s.{{%(target_field)s.predicted_value}}' % context,
                    'value': '{{%(field)s.default}}' % context,
                    'override': False,
                },
            }


PublicationIndex = PublicationIndex(name='publications')


@PublicationIndex.document
class PublicationDocument(Document):
    title = TranslationField()
    subtitle = TranslationField()
    abstract = TranslationField()

    class Django:
        model = Publication
        fields = [
            'ris_type',
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

    def update(self, *args, **kwargs):
        kwargs.setdefault('pipeline', 'language-detection')

        return super(PublicationDocument, self).update(*args, **kwargs)
