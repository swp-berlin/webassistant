from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.indices import Index

from elasticsearch.client.ingest import IngestClient

from swp.models import Publication, Thinktank

from .fields import ANALYZERS, FieldMixin, get_translation_fields

LANGUAGES = [*ANALYZERS]

TRANSLATION_FIELDS = [
    'title',
    'subtitle',
    'abstract',
]


class PublicationIndex(Index):

    def create(self, using=None, **kwargs):
        result = Index.create(self, using=using, **kwargs)

        self.add_language_detection(*TRANSLATION_FIELDS)

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
class PublicationDocument(FieldMixin, Document):
    TRANSLATION_FIELDS = TRANSLATION_FIELDS

    ttid = fields.IntegerField(attr='thinktank.id')
    ttname = fields.TextField(attr='thinktank.name')
    thinktank = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
    })

    class Django:
        model = Publication
        related_models = [
            Thinktank,
        ]
        fields = [
            'title',
            'subtitle',
            'abstract',
            'ris_type',
            'authors',
            'publication_date',
            'publication_dt',
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

    def get_queryset(self):
        return Publication.objects.select_related('thinktank')

    @staticmethod
    def get_instances_from_related(related_instance):
        if isinstance(related_instance, Thinktank):
            return related_instance.publications.all()

    @classmethod
    def to_field(cls, field_name, model_field):
        if field_name == 'tags':
            base_field = fields.KeywordField(attr=field_name)

            return fields.ListField(base_field)

        return super().to_field(field_name, model_field)

    def update(self, *args, **kwargs):
        kwargs.setdefault('pipeline', 'language-detection')

        return super().update(*args, **kwargs)

    @classmethod
    def get_search_fields(cls, language):
        return [*get_translation_fields(language, cls.TRANSLATION_FIELDS), 'authors', 'isbn', 'tags']
