from django.db import models
from django.utils.translation import gettext as _

from base.models import CoreModel
from core.choices import WorkspaceSysname


class Workspace(CoreModel):
    name: str = models.CharField(_("Название"), max_length=256)
    sys_name: str = models.CharField(
        _("Системное имя"), choices=WorkspaceSysname, max_length=256, null=True, blank=True, unique=True
    )

    class Meta:
        verbose_name = _("Пространство")
        verbose_name_plural = _("Пространства")

    def __str__(self) -> str:
        return self.name
