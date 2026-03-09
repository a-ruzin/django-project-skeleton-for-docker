from django.db import transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.request import Request
from rest_framework.response import Response

from base.serializers import ErrorSerializer
from core.api.errors import ErrorCode
from core.api.v1.mixins import CoreApiResponseMixin
from core.api.v1.serializers.user import UserSerializer
from core.controllers.user_registration_request_controller import UserRegistrationRequestController
from core.models import UserRegistrationRequest


class ConfirmRegistrationByTokenView(CoreApiResponseMixin, generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_summary="Confirm registration by token",
        operation_description="Подтверждает регистрацию по длинному токену (например, из email) и создаёт пользователя.",
        manual_parameters=[
            openapi.Parameter(
                name="uuid",
                in_=openapi.IN_PATH,
                description="Registration request UUID",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                name="token",
                in_=openapi.IN_PATH,
                description="Confirmation token (long)",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            201: openapi.Response(
                description="Registration confirmed",
                schema=UserSerializer,
            ),
            400: openapi.Response(
                description="Invalid or expired token/request",
                schema=ErrorSerializer,
            ),
        },
        tags=["auth"],
    )
    def get(self, request: Request, user_registration_id: PrimaryKey, token: PrimaryKey) -> Response:
        try:
            registration = UserRegistrationRequest.objects.is_active().get(
                id=user_registration_id,
                phone_confirmation_token=token,
            )
        except UserRegistrationRequest.DoesNotExist:
            return self.get_error_response_from_code(ErrorCode.EXPIRED_REGISTRATION_REQUEST)

        with transaction.atomic():
            user = UserRegistrationRequestController.create_user(registration)
            registration.delete()

        output_serializer = UserSerializer(
            user,
            context=self.get_serializer_context(),
        )
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
