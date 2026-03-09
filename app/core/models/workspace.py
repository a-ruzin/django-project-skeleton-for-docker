from django.db import models
from django.utils.translation import gettext as _

from base.models import CoreModel
from core.models.querysets import WorkspaceQuerySet


def get_slug() -> str:
    import secrets

    return secrets.token_urlsafe()[:8]


class Workspace(CoreModel):
    name = models.CharField(_("Название"), max_length=256)
    slug = models.CharField(_("Системное имя"), max_length=64, unique=True, default=get_slug)
    owner = models.ForeignKey("core.User", verbose_name=_("Владелец"), on_delete=models.PROTECT, related_name="owned_workspaces")

    objects = WorkspaceQuerySet.as_manager()

    class Meta:
        verbose_name = _("Пространство")
        verbose_name_plural = _("Пространства")
        unique_together = ("slug",)

    def __str__(self) -> str:
        return self.name
