from django.db import models
from django.db.models.functions import Greatest
from django.http import Http404
from django.utils.text import slugify

from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.viewsets import ModelViewSet

from swp.api import default_router
from swp.api.serializers import PublicationListSerializer, PublicationListDetailSerializer
from swp.models import PublicationList, Publication, PublicationListEntry
from swp.utils.ris import RISResponse

LAST_UPDATED_PUBLICATION_LIST = f'{0}'


@default_router.register('publication-list', basename='publication-list')
class PublicationListViewSet(ModelViewSet):
    serializer_class = PublicationListSerializer
    queryset = PublicationList.objects.annotate(
        entry_count=models.Count('entries'),
        last_updated=Greatest(
            models.F('last_modified'),
            models.Max('entries__created'),
        ),
    )

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user).order_by('-last_updated')

        if self.action == 'retrieve':
            return queryset.prefetch_related('publications')

        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PublicationListDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    @action(detail=True, url_path=r'add/(?P<publication>\d+)')
    def add(self, request, *, pk: str, publication: str):
        publication_list = self.get_publication_list(pk)
        publication = get_object_or_404(Publication, id=publication)

        PublicationListEntry.objects.create(
            publication_list=publication_list,
            publication=publication,
            created=request.now,
        )

        return Response(status=HTTP_201_CREATED)

    @action(detail=True, url_path=r'remove/(?P<publication>\d+)')
    def remove(self, request, *, pk: str, publication: str):
        publication_list = self.get_object()
        publication = get_object_or_404(Publication, id=publication)

        PublicationListEntry.objects.filter(
            publication_list=publication_list,
            publication=publication,
        ).delete()

        return Response(status=HTTP_204_NO_CONTENT)

    @action(detail=True)
    def export(self, request, **kwargs):
        publication_list = self.get_object()
        publications = publication_list.publications.all()
        filename = '%s.ris' % slugify(publication_list.name)

        return RISResponse(publications, filename)

    def get_publication_list(self, pk: str):
        if pk == LAST_UPDATED_PUBLICATION_LIST:
            try:
                return self.queryset.latest('last_updated')
            except PublicationList.DoesNotExist:
                raise Http404

        return self.get_object()
