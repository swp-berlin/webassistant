from functools import wraps

from django.contrib.postgres.aggregates import ArrayAgg
from django.db import models, transaction
from django.db.models.functions import Greatest, Upper
from django.utils.text import slugify

from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_202_ACCEPTED
from rest_framework.viewsets import ModelViewSet

from swp.api import default_router
from swp.api.serializers import PublicationListSerializer, PublicationListDetailSerializer
from swp.models import PublicationList, Publication, PublicationListEntry
from swp.utils.ris import RISResponse


def publication_action(handler):
    @action(['POST'], detail=True, url_path=rf'{handler.__name__}/(?P<publication>\d+)')
    @transaction.atomic
    @wraps(handler)
    def wrapper(self, request, *, pk: str, publication: str):
        publication_list = self.get_object()
        publication = get_object_or_404(Publication, id=publication)
        status = handler(self, request, publication_list, publication)
        serializer = self.get_serializer(publication_list)

        return Response(serializer.data, status=status)

    return wrapper


@default_router.register('publication-list', basename='publication-list')
class PublicationListViewSet(ModelViewSet):
    serializer_class = PublicationListSerializer
    queryset = PublicationList.objects.annotate(
        entry_count=models.Count('entries'),
        publication_list=ArrayAgg('entries__publication'),
        last_updated=Greatest(
            models.F('last_modified'),
            models.Max('entries__created'),
        ),
    ).order_by(
        Upper('name').asc(),
    )

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)

        if self.action == 'retrieve':
            return queryset.prefetch_related('publications')

        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PublicationListDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    @publication_action
    def add(self, request, publication_list, publication):
        PublicationListEntry.objects.create(
            publication_list=publication_list,
            publication=publication,
            created=request.now,
        )

        publication_list.entry_count += 1
        publication_list.publication_list.append(publication.id)
        publication_list.last_updated = request.now

        return HTTP_201_CREATED

    @publication_action
    def remove(self, request, publication_list, publication):
        deleted, objs = PublicationListEntry.objects.filter(
            publication_list=publication_list,
            publication=publication,
        ).delete()

        if deleted:
            publication_list.entry_count -= 1
            publication_list.publication_list.remove(publication.id)
            PublicationList.objects.filter(id=publication_list.id).update(last_modified=publication_list.last_updated)

        return HTTP_202_ACCEPTED

    @action(detail=True)
    def export(self, request, **kwargs):
        publication_list = self.get_object()
        publications = publication_list.publications.all()
        filename = '%s.ris' % slugify(publication_list.name)

        return RISResponse(publications, filename)
