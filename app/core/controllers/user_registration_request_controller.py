from django.conf import settings
from django.urls import reverse

from core.controllers.sms_controller import SmsController
from core.models import User
from core.models.user_registration_request import UserRegistrationRequest
from lib.sms import SmsService, SmsServiceConfig


class UserRegistrationRequestController:
    @staticmethod
    def create_user(user_registration_request: UserRegistrationRequest):
        return User.objects.create_user(
            email=user_registration_request.email,
            phone=user_registration_request.phone,
            is_phone_confirmed=True,
            password=user_registration_request.password,
            ip_address=user_registration_request.ip_address,
        )

    @classmethod
    def send_verification_token(cls, user_registration_request: UserRegistrationRequest):
        # url = reverse('core:api:v1:confirm-user-registration-by-token', args=[user_registration_request.phone_confirmation_token])
        SmsController.send_sms(user_registration_request.phone, f"Код подтверждения: {user_registration_request.phone_confirmation_code}")
