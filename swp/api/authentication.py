from django.conf import settings

from rest_framework import authentication


class SessionAuthentication(authentication.SessionAuthentication):
    """
    This authentication returns an authentication header so an unauthorized
    request is properly answered with a 401 instead of an 403.
    """

    def authenticate_header(self, request):
        return f'Cookie name={settings.SESSION_COOKIE_NAME}'
