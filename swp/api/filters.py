from typing import Iterable

from django_filters.rest_framework import BooleanFilter
from django.utils.translation import gettext_lazy as _

from swp.models import PublicationCount
from swp.tasks import update_publication_count


class UpdatePublicationCountFilter(BooleanFilter):
    label = _('update publication count')

    def filter(self, qs: Iterable[PublicationCount], update):
        if update:
            for obj in qs:
                update_publication_count.delay(obj._meta.label, obj.pk)

        return qs
