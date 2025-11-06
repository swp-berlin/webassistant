from typing import cast

from django_elasticsearch_dsl.search import Search
from elasticsearch.exceptions import BadRequestError

from rest_framework.exceptions import APIException

from swp.api.v1.pagination import SWPagination
from swp.documents import PublicationDocument


class ElasticSearchException(APIException):

    def __init__(self, error: BadRequestError):
        self.status_code = error.status_code
        self.default_code = error.message

        if isinstance(error.body, dict):
            error = error.body.get('error', error.body)

        APIException.__init__(self, error)


class ElasticSearchPagination(SWPagination):

    def paginate_queryset(self, queryset, request, view=None, *, using=None, keep_search_order=True):
        search = PublicationDocument.search(using=using).update_from_dict(request.data).source(False)

        try:
            super().paginate_queryset(search, request, view=view)
        except BadRequestError as error:
            raise ElasticSearchException(error) from error

        return cast(Search, search).filter_queryset(queryset, keep_search_order=keep_search_order)
