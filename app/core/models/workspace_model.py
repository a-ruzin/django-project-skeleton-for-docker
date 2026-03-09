from django.db import models
from django.utils.translation import gettext as _

from base.models import CoreModel


class WorkspaceModel(CoreModel):
    """
    Абстрактная модель, привязанная к рабочему пространству
    """
    class Meta:
        abstract = True

    workspace = models.ForeignKey(_("Workspace"), null=False, related_name="%(app_label)s_%(class)s", on_delete=models.PROTECT)  # type: ignore
