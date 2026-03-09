from typing import Union, TYPE_CHECKING

from django.db.models import Q
from django.utils import timezone

from base.models.conditions import condition

if TYPE_CHECKING:
    from core.models.user_registration_request import UserRegistrationRequest


@condition
def is_expired(model_instance: Union["UserRegistrationRequest", None] = None) -> Union[bool, Q]:
    if model_instance is not None:
        return model_instance.expires_at < timezone.now()
    else:
        return Q(expires_at__lt=timezone.now())
