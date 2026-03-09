from typing import Self

from base.models.querysets.core_base_queryset import CoreBaseQuerySet
from core.models.conditions.user_registration_request_condition import is_expired


class UserRegistrationRequestQuerySet(CoreBaseQuerySet):
    def is_expired(self) -> Self:
        return self.filter(is_expired())

    def is_active(self) -> Self:
        return self.exclude(is_expired())
