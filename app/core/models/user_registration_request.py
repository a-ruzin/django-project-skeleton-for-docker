import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models import CoreModel
from core.models.conditions.user_registration_request_condition import is_expired
from core.models.querysets import UserRegistrationRequestQuerySet


def get_confirmation_code() -> str:
    import secrets

    return f"{int(secrets.token_hex()[:5], 16)%1000000:06}"


class UserRegistrationRequest(CoreModel):
    """Temporary storage for unconfirmed registrations"""
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)

    phone_confirmation_token = models.UUIDField(default=uuid.uuid4, unique=True)
    phone_confirmation_code = models.CharField(_("Короткий код подтверждения"), max_length=6, default=get_confirmation_code)

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    expires_at = models.DateTimeField()

    objects = UserRegistrationRequestQuerySet.as_manager()

    class Meta:
        verbose_name = _("Запрос на регистрацию пользователя")
        verbose_name_plural = _("Запросы на регистрацию пользователей")

    def is_expired(self):
        return is_expired(self)
