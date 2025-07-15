from typing import Any

from ..querysets.soft_deletion_queryset import SoftDeletionQuerySet
from .core_base_manager import CoreBaseManager


class SoftDeletionManager(CoreBaseManager):
    queryset_class = SoftDeletionQuerySet

    def get_queryset(self) -> SoftDeletionQuerySet:
        return self.queryset_class(self.model)

    def hard_delete(self) -> Any:
        return self.get_queryset().hard_delete()
