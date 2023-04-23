__all__ = ['UserQuerySet']

from typing import Any

from base.models.querysets.core_base_queryset import CoreBaseQuerySet


class UserQuerySet(CoreBaseQuerySet):
    def active(self) -> Any:
        return self.filter(is_active=True)
