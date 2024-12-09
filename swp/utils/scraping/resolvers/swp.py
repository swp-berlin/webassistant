from swp.utils.isbn import canonical_isbn

from .field import FieldResolver


class TitleResolver(FieldResolver):
    key = 'title'


class SubtitleResolver(FieldResolver):
    key = 'subtitle'


class AbstractResolver(FieldResolver):
    key = 'abstract'


class PublicationDateResolver(FieldResolver):
    key = 'publication_date'


class URLResolver(FieldResolver):
    key = 'url'


class AuthorsResolver(FieldResolver):
    key = 'authors'
    multiple = True
    ignore_empty = True


class TagsResolver(FieldResolver):
    key = 'tags'
    multiple = True


class DOIResolver(FieldResolver):
    key = 'doi'


class ISBNResolver(FieldResolver):
    key = 'isbn'
    normalize = staticmethod(canonical_isbn)
