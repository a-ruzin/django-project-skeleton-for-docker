from typing import Self, TYPE_CHECKING

from base.models.querysets.core_base_queryset import CoreBaseQuerySet

if TYPE_CHECKING:
    from core.models import User


class WorkspaceQuerySet(CoreBaseQuerySet):
    def accessible_to_user(self, user: "User") -> Self:
        return self.filter(
            user_roles__user=user
        ) | self.filter(
            owner=user
        )
