from django.db import models
from django.utils.translation import gettext as _

from core.models.workspace_model import WorkspaceModel


class Thing(WorkspaceModel):
    # TODO: это модель для примера, удалите или переименуйте ее
    #  Она нужна для демонстрации того, как работать с моделями,
    #  привязанными к рабочему пространству
    payload = models.CharField(_("Что-то полезное"), max_length=256)


    class Meta:
        verbose_name = _("Штука")
        verbose_name_plural = _("Штуки")

    def __str__(self) -> str:
        return self.payload
