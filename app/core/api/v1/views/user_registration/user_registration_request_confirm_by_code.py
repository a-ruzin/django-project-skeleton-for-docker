from django.conf import settings
from django.db import transaction
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from base.serializers import ErrorSerializer
from core.api.errors import ErrorCode
from core.api.v1.mixins import CoreApiResponseMixin
from core.api.v1.serializers.user import UserSerializer
from core.api.v1.serializers.user_registration import ConfirmationByCodeSerializer
from core.controllers.user_registration_request_controller import UserRegistrationRequestController
from core.models import UserRegistrationRequest


class ConfirmRegistrationByCodeView(CoreApiResponseMixin, generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ConfirmationByCodeSerializer

    @swagger_auto_schema(
        operation_summary="Confirm user_registration_request by short code",
        operation_description="Подтверждает регистрацию по короткому коду (например, из SMS) и создаёт пользователя.",
        manual_parameters=[
            openapi.Parameter(
                name="user_registration_id",
                in_=openapi.IN_PATH,
                description="Registration request UUID",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        request_body=ConfirmationByCodeSerializer,
        responses={
            201: openapi.Response(
                description="Registration confirmed",
                schema=UserSerializer,
            ),
            400: openapi.Response(
                description="Invalid/expired request or invalid code",
                schema=ErrorSerializer,
            ),
        },
        tags=["auth"],
    )
    def post(self, request: Request, user_registration_id: PrimaryKey) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data["code"]

        try:
            user_registration_request = UserRegistrationRequest.objects.is_active().get(id=user_registration_id)
        except UserRegistrationRequest.DoesNotExist:
            return self.get_error_response_from_code(ErrorCode.EXPIRED_REGISTRATION_REQUEST)

        good_codes = [user_registration_request.phone_confirmation_code]
        if settings.DEBUG_PHONE_CONFIRMATION_CODE:
            good_codes.append(settings.DEBUG_PHONE_CONFIRMATION_CODE)
        if code not in good_codes:
            return self.get_error_response_from_code(ErrorCode.WRONG_CONFIRMATION_CODE)

        with transaction.atomic():
            user = UserRegistrationRequestController.create_user(user_registration_request)
            user_registration_request.delete()

        # Выпускаем JWT-токены для нового пользователя
        refresh = RefreshToken.for_user(user)

        output_serializer = UserSerializer(
            user,
            context=self.get_serializer_context(),
        )
        response = Response(output_serializer.data, status=status.HTTP_201_CREATED)

        # Устанавливаем HttpOnly cookies (как при логине)
        jwt = settings.SIMPLE_JWT
        response.set_cookie(
            key=jwt['AUTH_COOKIE'],
            value=str(refresh.access_token),
            expires=timezone.now() + jwt['ACCESS_TOKEN_LIFETIME'],
            secure=jwt['AUTH_COOKIE_SECURE'],
            httponly=jwt['AUTH_COOKIE_HTTP_ONLY'],
            samesite=jwt['AUTH_COOKIE_SAMESITE'],
            path=jwt['AUTH_COOKIE_PATH'],
        )
        response.set_cookie(
            key=jwt['AUTH_COOKIE_REFRESH'],
            value=str(refresh),
            expires=timezone.now() + jwt['REFRESH_TOKEN_LIFETIME'],
            secure=jwt['AUTH_COOKIE_SECURE'],
            httponly=jwt['AUTH_COOKIE_HTTP_ONLY'],
            samesite=jwt['AUTH_COOKIE_SAMESITE'],
            path=jwt['AUTH_COOKIE_PATH'],
        )

        return response
