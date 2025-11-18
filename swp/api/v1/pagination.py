from rest_framework.pagination import LimitOffsetPagination


class SWPagination(LimitOffsetPagination):
    default_limit = max_limit = 100
