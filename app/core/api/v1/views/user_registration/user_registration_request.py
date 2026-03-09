from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from base.serializers import ErrorSerializer
from core.api.errors import ErrorCode
from core.api.v1.mixins import CoreApiResponseMixin
from core.api.v1.serializers.user_registration import (
    UserRegistrationRequestSerializer,
    UserRegistrationRequestSerializerForCreate,
)
from core.controllers.user_registration_request_controller import UserRegistrationRequestController
from core.models import UserRegistrationRequest
from core.models.user_registration_request import get_confirmation_code


class UserRegistrationRequestView(CoreApiResponseMixin, generics.CreateAPIView):
    """
    Anyone can create a registration request
    """
    queryset = UserRegistrationRequest.objects.all()
    serializer_class = UserRegistrationRequestSerializerForCreate
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_summary="Create registration request",
        operation_description=(
                "Создаёт заявку на регистрацию и отправляет токен подтверждения. "
                "Если пользователь уже аутентифицирован — возвращает 403."
        ),
        request_body=UserRegistrationRequestSerializerForCreate,
        responses={
            201: openapi.Response(
                description="Registration request created",
                schema=UserRegistrationRequestSerializer,
            ),
            403: openapi.Response(
                description="Authenticated users cannot create new accounts",
                schema=ErrorSerializer,
            ),
            400: openapi.Response(
                description="Validation error",
                schema=ErrorSerializer,
            ),
        },
        tags=["auth"],
    )
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.get_error_response_from_code(ErrorCode.AUTHENTICATED_CANNOT_REGISTER)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']

        # Если уже есть активная заявка на этот телефон — обновляем код и переиспользуем
        existing_request = UserRegistrationRequest.objects.is_active().filter(phone=phone).first()
        if existing_request:
            existing_request.phone_confirmation_code = get_confirmation_code()
            existing_request.save(update_fields=['phone_confirmation_code'])
            user_registration_request = existing_request
        else:
            # Удаляем просроченные заявки для этого телефона (на случай unique constraint)
            UserRegistrationRequest.objects.is_expired().filter(phone=phone).delete()
            self.perform_create(serializer)
            user_registration_request = serializer.instance

        UserRegistrationRequestController.send_verification_token(user_registration_request)

        output_serializer = UserRegistrationRequestSerializer(
            user_registration_request,
            context=self.get_serializer_context(),
        )
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
