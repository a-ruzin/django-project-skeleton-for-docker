__all__ = ("SoftDeletionQuerySet",)

from typing import Any

from django.utils import timezone

from .core_base_queryset import CoreBaseQuerySet


class SoftDeletionQuerySet(CoreBaseQuerySet):
    def delete(self) -> Any:
        return self.update(deleted_at=timezone.now())

    def hard_delete(self) -> Any:
        return super().delete()

    def alive(self) -> Any:
        return self.filter(deleted_at=None)

    def dead(self) -> Any:
        return self.exclude(deleted_at=None)
