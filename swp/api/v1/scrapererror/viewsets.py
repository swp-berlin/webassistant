from django.utils.translation import gettext_lazy as _

from rest_framework.mixins import DestroyModelMixin
from rest_framework.viewsets import ReadOnlyModelViewSet

from swp.api.v1.viewsets import SWPViewSetMixin
from swp.models import ScraperError

from .filters import ScraperErrorFilterSet
from .serializers import ScraperErrorSerializer


@SWPViewSetMixin.register('scraper-error')
class ScraperErrorViewSet(SWPViewSetMixin, DestroyModelMixin, ReadOnlyModelViewSet):
    serializer_class = ScraperErrorSerializer
    queryset = ScraperError.objects
    filterset_class = ScraperErrorFilterSet
    ordering = ['-timestamp']
    ordering_fields = [
        ('id', _('ID')),
        ('timestamp', _('timestamp')),
    ]
