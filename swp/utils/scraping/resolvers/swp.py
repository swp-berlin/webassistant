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


class TagsResolver(FieldResolver):
    key = 'tags'
    multiple = True
