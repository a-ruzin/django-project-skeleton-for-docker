from django.db import models
from django.utils.translation import gettext as _

from base.models import CoreModel


class Sentinel(CoreModel):
    # TODO: это модель для примера, удалите или переименуйте ее
    user = models.ForeignKey(
        "core.User",
        on_delete=models.CASCADE,
        related_name="sentinels",
        verbose_name=_("Пользователь"),
    )
    payload = models.CharField(_("Что-то полезное"), max_length=256)


    class Meta:
        verbose_name = _("Заготовка")
        verbose_name_plural = _("Заготовки")

    def __str__(self) -> str:
        return self.payload
