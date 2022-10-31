from django.utils.timezone import localtime


def now(get_response):
    """
    Adds a timestamp to the request that should be used throughout the request lifecycle.
    """

    def inner(request, timezone=None):
        request.now = localtime(timezone=timezone)

        return get_response(request)

    return inner
