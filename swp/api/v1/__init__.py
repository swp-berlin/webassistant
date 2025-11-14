from rest_framework.serializers import ModelSerializer

from swp.models.fields import DomainField as ModelDomainField

from .fields import DomainField as SerializerDomainField
from .router import default_router

ModelSerializer.serializer_field_mapping[ModelDomainField] = SerializerDomainField

from .category import *
from .explorer import *
from .monitor import *
from .pool import *
from .publication import *
from .publicationlist import *
from .scraper import *
from .spectacular import *
from .thinktank import *
