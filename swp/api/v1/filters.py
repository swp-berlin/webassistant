from django_filters.rest_framework import BooleanFilter
from django.utils.translation import gettext_lazy as _


class UpdatePublicationCountFilter(BooleanFilter):
    label = _('update publication count')

    def filter(self, qs, update):
        if update:
            for filter in qs:
                filter.update_publication_count()

        return qs
