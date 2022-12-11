__all__ = ("SoftDeletionQuerySet",)

from django.utils import timezone

from .core_base_queryset import CoreBaseQuerySet


class SoftDeletionQuerySet(CoreBaseQuerySet):
    def delete(self):
        return self.update(deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)
