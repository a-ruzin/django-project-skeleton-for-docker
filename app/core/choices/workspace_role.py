from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class WorkspaceRole(TextChoices):
    """Типы ролей пользователей в пространстве"""

    ADMINISTRATOR = 'ADMINISTRATOR', _('ADMINISTRATOR')
    EMPLOYEE = 'EMPLOYEE', _('EMPLOYEE')
