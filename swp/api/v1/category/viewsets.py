from swp.api.v1.viewsets import SWPViewSet
from swp.models import Category

from .serializers import CategorySerializer


@SWPViewSet.register('category')
class CategoryViewSet(SWPViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects
