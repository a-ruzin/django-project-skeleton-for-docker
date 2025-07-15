from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class WorkspaceSysname(TextChoices):
    """Специальные системные имена пространств"""

    KOKOC_GROUP = 'kokoc_group', _('Kokoc Group')
