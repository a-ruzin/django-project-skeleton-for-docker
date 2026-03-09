from django.conf import settings

from lib.sms import SmsService, SmsServiceConfig


class SmsController:
    @classmethod
    def send_sms(cls, phone: str, message: str) -> None:
        SmsService(settings.SMS_SERVICE).send_sms(
            phone=phone,
            message=message
        )
