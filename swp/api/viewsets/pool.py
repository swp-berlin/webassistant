from django.utils.translation import gettext_lazy as _

from django_filters import FilterSet, BooleanFilter

from rest_framework.viewsets import ReadOnlyModelViewSet

from swp.api import default_router
from swp.api.serializers import PoolSerializer
from swp.models import Pool


class PoolFilterSet(FilterSet):
    can_manage = BooleanFilter(label=_('can manage'))

    class Meta:
        model = Pool
        fields = ['can_manage']


@default_router.register('pool', basename='pool')
class PoolViewSet(ReadOnlyModelViewSet):
    queryset = Pool.objects
    serializer_class = PoolSerializer
    filterset_class = PoolFilterSet

    def get_queryset(self):
        return ReadOnlyModelViewSet.get_queryset(self).annotate_can_manage(self.request.user)
