from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

from swp.models import AuthToken


class SessionAuthentication(authentication.SessionAuthentication):
    """
    This authentication returns an authentication header so an unauthorized
    request is properly answered with a 401 instead of an 403.
    """

    def authenticate_header(self, request):
        return f'Cookie name={settings.SESSION_COOKIE_NAME}'


class TokenAuthentication(authentication.TokenAuthentication):
    keyword = 'Bearer'
    model = AuthToken

    def authenticate(self, request):
        if auth := super().authenticate(request):
            user, token = auth

            if token.expires and token.expires < request.now:
                raise AuthenticationFailed(_('Token is expired.'))

        return auth

    def authenticate_credentials(self, key):
        try:
            return super().authenticate_credentials(key)
        except ValidationError as error:
            raise AuthenticationFailed(_('Invalid token header: %(error)s') % {'error': error})
