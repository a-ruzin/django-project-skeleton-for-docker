from django.conf import settings
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from base.serializers import ErrorSerializer
from core.api.v1.mixins import CoreApiResponseMixin


class CookieTokenObtainPairView(CoreApiResponseMixin, TokenObtainPairView):
    """
    Takes username/password and returns access/refresh tokens as HttpOnly cookies.
    """

    @swagger_auto_schema(
        operation_summary="JWT login (cookies)",
        operation_description=(
                "Аутентификация по логину и паролю. "
                "Токены **не возвращаются в JSON**, вместо этого сервер устанавливает "
                "`access` и `refresh` как **HttpOnly cookies**."
        ),
        # request_body=TokenObtainPair,
        responses={
            204: openapi.Response(
                description="Login successful. Tokens are set in HttpOnly cookies.",
                headers={
                    "Set-Cookie": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description=(
                                "Устанавливается как минимум 2 cookie: "
                                f"`{settings.SIMPLE_JWT.get('AUTH_COOKIE', '<ACCESS_COOKIE_NAME>')}` и "
                                f"`{settings.SIMPLE_JWT.get('AUTH_COOKIE_REFRESH', '<REFRESH_COOKIE_NAME>')}` "
                                "(HttpOnly, Secure/SameSite — по настройкам)."
                        ),
                    ),
                },
            ),
            400: openapi.Response(
                description="Validation error (bad request body)",
                schema=ErrorSerializer,
            ),
            401: openapi.Response(
                description="Invalid credentials",
                schema=ErrorSerializer,
            ),
        },
        tags=["token"],
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the tokens from the serializer
        access_token = serializer.validated_data.get("access")
        refresh_token = serializer.validated_data.get("refresh")

        # Create response
        response = Response(
            # {"detail": "Login successful", "access": access_token}, # Optionally return access for debugging, but not needed
            None,
            status=status.HTTP_204_NO_CONTENT
        )

        # Set HttpOnly cookies
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=access_token,
            expires=timezone.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
        )
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            value=refresh_token,
            expires=timezone.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
        )

        return response


class CookieTokenRefreshView(TokenRefreshView):
    """
    Takes refresh token from cookie and returns new access token.
    """

    @swagger_auto_schema(
        operation_summary="JWT refresh (cookies)",
        operation_description=(
                "Обновляет access-токен по refresh-токену из **HttpOnly cookie**. "
                "Тело запроса не требуется. "
                "Успешный ответ возвращает **204**, а новый access устанавливается в cookie. "
                "Если включён ROTATE_REFRESH_TOKENS — refresh cookie тоже может обновиться."
        ),
        request_body=no_body,
        responses={
            204: openapi.Response(
                description="Token refreshed successfully. New tokens are set in HttpOnly cookies.",
                headers={
                    "Set-Cookie": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description=(
                                "Обновляется cookie с access-токеном "
                                f"`{settings.SIMPLE_JWT.get('AUTH_COOKIE', '<ACCESS_COOKIE_NAME>')}`. "
                                "Если включён ROTATE_REFRESH_TOKENS — может обновиться и "
                                f"`{settings.SIMPLE_JWT.get('AUTH_COOKIE_REFRESH', '<REFRESH_COOKIE_NAME>')}`."
                        ),
                    ),
                },
            ),
            401: openapi.Response(
                description="Refresh token not found in cookies",
                schema=ErrorSerializer,
            ),
            400: openapi.Response(
                description="Invalid/expired refresh token",
                schema=ErrorSerializer,
            ),
        },
        tags=["token"],
    )
    def post(self, request, *args, **kwargs):
        # Get refresh token from cookie (not from request body)
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])

        if not refresh_token:
            return Response(
                {"detail": "Refresh token not found in cookies"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Pass the refresh token to the serializer
        serializer = self.get_serializer(data={"refresh": refresh_token})
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        access_token = data.get("access")
        new_refresh_token = data.get("refresh") # Only present if ROTATE_REFRESH_TOKENS is True

        response = Response(
            None, # {"detail": "Token refreshed"},
            status=status.HTTP_204_NO_CONTENT
        )

        # Set new access token cookie
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=access_token,
            expires=timezone.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
        )

        # If a new refresh token was issued, update the cookie
        if new_refresh_token:
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                value=new_refresh_token,
                expires=timezone.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
            )

        return response


class CookieTokenLogoutView(APIView):
    """
    Удаляет access и refresh токены из HttpOnly cookies.
    Опционально добавляет refresh token в blacklist.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="JWT logout (cookies)",
        operation_description=(
            "Удаляет access и refresh токены из HttpOnly cookies. "
            "Refresh-токен добавляется в blacklist. "
            "Тело запроса не требуется."
        ),
        request_body=no_body,
        responses={
            204: openapi.Response(
                description="Logout successful. Token cookies have been deleted.",
            ),
        },
        tags=["token"],
    )
    def post(self, request, *args, **kwargs):
        # Блэклистим refresh token, если он есть
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except TokenError:
                pass  # Токен уже невалиден — ничего страшного

        response = Response(None, status=status.HTTP_204_NO_CONTENT)

        response.delete_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
        )
        response.delete_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
        )

        return response
