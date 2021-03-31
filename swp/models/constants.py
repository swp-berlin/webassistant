
#: Extended length for :class:`~django.db.models.fields.URLField`
MAX_URL_LENGTH: int = 1024

#: Maximum length of a publication title
MAX_TITLE_LENGTH: int = 255

#: Maximum length of a single publication tag
MAX_TAG_LENGTH: int = 255

#: Length of human-readable ISBN identifier
MAX_ISBN_LENGTH: int = len('0 7 6 5-3 4 8 2 7 6')

#: Length of human-readable ISSN identifier
MAX_ISSN_LENGTH: int = len('2049-3630')

#: Maximum length of combined ISBN/ISSN identifier
MAX_COMBINED_ISBN_LENGTH: int = max(MAX_ISBN_LENGTH, MAX_ISSN_LENGTH)

