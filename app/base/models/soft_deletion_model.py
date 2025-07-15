from typing import Any

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .core_model import CoreModel
from .managers.soft_deletion_manager import SoftDeletionManager


class SoftDeletionBase(CoreModel):
    deleted_at = models.DateTimeField(_("дата удаления"), blank=True, null=True)

    objects = SoftDeletionManager()

    class Meta:
        abstract = True

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def delete(self, **kwargs: Any) -> None:
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self) -> Any:
        return super().delete()


class SoftDeletionModel(SoftDeletionBase, CoreModel):
    class Meta:
        abstract = True
