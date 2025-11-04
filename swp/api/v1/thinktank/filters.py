from swp.api.v1.filters import SWPFilterSet
from swp.models import Thinktank


class ThinktankFilterSet(SWPFilterSet):

    class Meta:
        model = Thinktank
        fields = [
            'name',
            'pool',
            'domain',
            'is_active',
        ]
