from rest_framework import filters, viewsets
from cosmogo.utils.settings import truthy

from swp.api.v1.router import router
from swp.api.v1.serializers import ThinktankSerializer
from swp.models import Thinktank


@router.register('thinktank', basename='thinktank')
class ThinktankViewSet(viewsets.ModelViewSet):
    queryset = Thinktank.objects.annotate_last_run().annotate_counts()
    serializer_class = ThinktankSerializer
    filter_backends = [filters.OrderingFilter]

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=truthy(is_active))

        return queryset
