from django.db import models
from django.utils.translation import gettext as _

from core.choices import WorkspaceRole
from core.models.workspace_model import WorkspaceModel


class WorkspaceUserRole(WorkspaceModel):
    workspace = models.ForeignKey("core.Workspace", on_delete=models.CASCADE, related_name="user_roles")
    user = models.ForeignKey("core.User", on_delete=models.CASCADE, related_name="workspace_roles")
    role = models.CharField(_("Роль"), max_length=256, choices=WorkspaceRole)

    class Meta:
        verbose_name = _("Роль пользователя")
        verbose_name_plural = _("Роли пользователей")
        unique_together = ("user", "workspace")

    def __str__(self) -> str:
        return f"{self.user} как {self.get_role_display()} в {self.workspace.name}"
