from rest_framework.viewsets import ModelViewSet

from swp.models import Scraper

from ..serializers import ScraperSerializer
from ..router import router


@router.register('scraper', basename='scraper')
class ScraperViewSet(ModelViewSet):
    queryset = Scraper.objects.all()
    serializer_class = ScraperSerializer
