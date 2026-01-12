from django.contrib.staticfiles.storage import staticfiles_storage
from django.db.models import Prefetch
from django.utils.functional import lazy

from drf_spectacular.utils import extend_schema

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from swp.api.permissions import CanResearch
from swp.api.v1.viewsets import SWPViewSet
from swp.models import Category, Publication, Scraper
from swp.utils.text import paragraph
from swp.utils.url import get_absolute_url

from .filters import PublicationFilterSet
from .pagination import ElasticSearchPagination
from .parsers import ElasticSearchQueryParser
from .serializers import PublicationSerializer, PublicationSearchSerializer


@SWPViewSet.register('publication')
class PublicationViewSet(SWPViewSet):
    serializer_class = PublicationSerializer
    filterset_class = PublicationFilterSet
    ordering_fields = [
        'id',
        'title',
        'created',
    ]
    queryset = Publication.objects.prefetch_related(
        Prefetch('scrapers', Scraper.objects.only('id')),
        Prefetch('categories', Category.objects.only('id')),
    )

    @extend_schema(
        responses=PublicationSerializer(many=True),
        description=paragraph(
            'This endpoint expects a [ElasticSearch Query object](https://www.elastic.co/docs/explore-analyze/query-filter/languages/querydsl).',
            'It is passed through to the underlying ElasticSearch engine.',
            'Refer to the docs on the available fields to query.'
        ),
        external_docs={
            'url': lazy(get_absolute_url, str)(None, staticfiles_storage.url('documents/helptext.pdf')),
            'description': 'Docs (HelpText.pdf)',
        },
    )
    @action(
        detail=False,
        methods=['POST'],
        filter_backends=[],
        parser_classes=[ElasticSearchQueryParser],
        pagination_class=ElasticSearchPagination,
        serializer_class=PublicationSearchSerializer,
        permission_classes=[IsAuthenticated & CanResearch],
    )
    def search(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
