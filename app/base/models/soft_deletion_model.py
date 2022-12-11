from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers.soft_deletion_manager import SoftDeletionManager
from .core_model import CoreModel


class SoftDeletionBase(CoreModel):
    deleted_at = models.DateTimeField(_('дата удаления'), blank=True, null=True)

    objects = SoftDeletionManager()

    class Meta:
        abstract = True

    @property
    def is_deleted(self):
        return self.deleted_at is not None

    def delete(self, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super().delete()


class SoftDeletionModel(SoftDeletionBase, CoreModel):
    class Meta:
        abstract = True
