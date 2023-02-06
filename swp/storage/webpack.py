from django.contrib.staticfiles.storage import StaticFilesStorage

from swp.utils.webpack import get_asset


class WebPackStorage(StaticFilesStorage):
    """
    A static file storage that could map webpack
    assets to their hash named url's.
    """

    def url(self, name):
        """
        Try to look up the name in the webpack asset mapping
        and return the url containing the current hash.
        """

        name = get_asset(name) or name

        return super(WebPackStorage, self).url(name)
