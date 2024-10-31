from django.db.models.functions import Lower
from rest_framework.decorators import action

from rest_framework.viewsets import ReadOnlyModelViewSet

from swp.api import default_router
from swp.api.serializers import CategorySerializer, CategoryChoiceSerializer
from swp.models import Category


@default_router.register('category', basename='category')
class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.order_by(Lower('name').asc())
    serializer_class = CategorySerializer

    @action(detail=False, serializer_class=CategoryChoiceSerializer)
    def choices(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
