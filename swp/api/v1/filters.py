from django.utils.translation import gettext_lazy as _

from django_filters import rest_framework as filters


class SWPFilterSet(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains', label=_('name'))
