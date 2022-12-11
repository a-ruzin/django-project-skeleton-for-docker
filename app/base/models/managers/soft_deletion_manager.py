__all__ = ("SoftDeletionManager",)

from .core_base_manager import CoreBaseManager
from ..querysets.soft_deletion_queryset import SoftDeletionQuerySet


class SoftDeletionManager(CoreBaseManager):
    queryset_class = SoftDeletionQuerySet

    def get_queryset(self):
        return self.queryset_class(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()
