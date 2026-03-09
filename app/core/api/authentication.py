from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings


class CookieJWTAuthentication(JWTAuthentication):
    """
    JWTAuthentication, который берёт access token из HttpOnly cookie,
    а не из заголовка Authorization.
    """

    def authenticate(self, request):
        # Сначала пробуем стандартный заголовок Authorization
        header = self.get_header(request)
        if header is not None:
            raw_token = self.get_raw_token(header)
            if raw_token is not None:
                validated_token = self.get_validated_token(raw_token)
                return self.get_user(validated_token), validated_token

        # Если заголовка нет — пробуем cookie
        raw_token = request.COOKIES.get(settings.SIMPLE_JWT.get('AUTH_COOKIE'))
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token.encode() if isinstance(raw_token, str) else raw_token)
        return self.get_user(validated_token), validated_token
