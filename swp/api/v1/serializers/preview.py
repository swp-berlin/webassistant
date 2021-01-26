from rest_framework.fields import CharField, JSONField, SerializerMethodField
from rest_framework.serializers import Serializer

from swp.api.v1.serializers.scraper import ResolverConfigSerializer
from swp.tasks.scraper import preview_scraper


class PreviewSerializer(Serializer):
    id = CharField(read_only=True)
    status = CharField(read_only=True)
    publications = SerializerMethodField(read_only=True, method_name='get_publications')
    traceback = CharField(read_only=True)

    start_url = CharField(write_only=True)
    data = ResolverConfigSerializer(write_only=True)

    def save(self, **kwargs):
        self.instance = self.preview_scraper(**self.validated_data)

        return self.instance

    @staticmethod
    def preview_scraper(*, start_url, data, **kwargs):
        return preview_scraper.delay(start_url, data)

    def get_publications(self, result):
        if result.successful():
            return result.get(propagate=False)

        return None
