from django.db import models
from django.db.models.functions import Greatest

from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action

from swp.api.v1.publication import PublicationViewSet
from swp.api.v1.viewsets import SWPViewSet
from swp.models import PublicationList, PublicationListEntry

from .serializers import (
    PublicationListSerializer,
    PublicationListWithObjectsSerializer,
    PublicationListAddSerializer,
    PublicationListRemoveSerializer,
)


@SWPViewSet.register('publication-list', basename='publication-list')
class PublicationListViewSet(SWPViewSet):
    serializer_class = PublicationListSerializer
    queryset = PublicationList.objects.prefetch_related('entries').annotate(
        last_updated=Greatest(
            models.F('last_modified'),
            models.Max('entries__created'),
        ),
    )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @extend_schema(
        operation_id='publication_list_with_objects',
        description='Endpoint to retrieve a list of publication lists with publications as objects.',
    )
    @action(
        detail=False,
        url_path='with-objects',
        serializer_class=PublicationListWithObjectsSerializer,
        queryset=queryset.prefetch_related(None).prefetch_related(
            models.Prefetch('entries', PublicationListEntry.objects.prefetch_related(
                models.Prefetch('publication', PublicationViewSet.queryset),
            )),
        ),
    )
    def with_objects(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        operation_id='publication_list_add_publication',
        description='Endpoint to add a publication to a list.',
    )
    @action(['POST'], detail=True, serializer_class=PublicationListAddSerializer)
    def add(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        operation_id='publication_list_remove_publication',
        description='Endpoint to remove a publication from a list.',
    )
    @action(['POST'], detail=True, serializer_class=PublicationListRemoveSerializer)
    def remove(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
