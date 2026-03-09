from rest_framework.permissions import BasePermission

from core.api.errors import ErrorCode, ERRORS
from core.models import WorkspaceUserRole


class ErrorCodePermission(BasePermission):
    """
    Базовый класс для permissions с поддержкой ErrorCode.

    DRF использует атрибут `message` для формирования PermissionDenied.
    Мы делаем `message` property, которое возвращает структурированный dict с error_code.

    Использование:
        class MyPermission(ErrorCodePermission):
            error_code = ErrorCode.WORKSPACE_ACCESS_DENIED

            def has_permission(self, request, view):
                if not check_permission():
                    return False  # DRF использует self.message для ошибки
                return True
    """
    error_code: ErrorCode = None

    @property
    def message(self):
        """
        DRF использует этот атрибут при создании PermissionDenied.
        Возвращаем структурированный dict с error_code и message.
        """
        if self.error_code and self.error_code in ERRORS:
            error_spec = ERRORS[self.error_code]
            return {
                'error_code': int(self.error_code),
                'message': str(error_spec.message),
            }
        return "Permission denied"


class IsWorkspaceOwner(BasePermission):
    """
    Разрешает действие только владельцу workspace.
    """
    message = "Только владелец пространства может выполнять это действие."

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class HasWorkspaceAccess(ErrorCodePermission):
    """
    Проверяет, что пользователь имеет доступ к workspace.
    Доступ есть у владельца или пользователей с ролью в workspace.

    При отказе в доступе возвращает структурированную ошибку с ErrorCode.WORKSPACE_ACCESS_DENIED
    """
    error_code = ErrorCode.WORKSPACE_ACCESS_DENIED

    def has_permission(self, request, view):
        """Проверка на уровне view - есть ли доступ к workspace вообще"""
        if not hasattr(view, 'get_workspace'):
            return True  # Если ViewSet не workspace-scoped, пропускаем проверку

        try:
            # get_workspace сам проверит доступ через accessible_to_user
            view.get_workspace()
            return True
        except Exception:
            # Возвращаем False, DRF автоматически вызовет permission_denied()
            return False


class HasWorkspaceRole(ErrorCodePermission):
    """
    Проверяет, что пользователь имеет одну из указанных ролей в workspace.

    При отказе возвращает структурированную ошибку с ErrorCode.WORKSPACE_INSUFFICIENT_PERMISSIONS

    Использование:
        class MyViewSet(ViewSet):
            permission_classes = [HasWorkspaceRole]
            required_workspace_roles = [WorkspaceRole.ADMINISTRATOR]
    """
    error_code = ErrorCode.WORKSPACE_INSUFFICIENT_PERMISSIONS

    def has_permission(self, request, view):
        """Проверка на уровне view"""
        if not hasattr(view, 'get_workspace'):
            return True

        workspace = view.get_workspace()
        required_roles = getattr(view, 'required_workspace_roles', None)

        if not required_roles:
            # Если роли не указаны, достаточно просто иметь доступ к workspace
            return True

        # Владелец всегда имеет доступ
        if workspace.owner == request.user:
            return True

        # Проверяем роль пользователя
        user_role = WorkspaceUserRole.objects.filter(
            workspace=workspace,
            user=request.user,
            role__in=required_roles
        ).exists()

        # Возвращаем результат проверки, DRF автоматически вызовет permission_denied() если False
        return user_role

    def has_object_permission(self, request, view, obj):
        """Проверка на уровне объекта"""
        # Проверяем, что объект принадлежит текущему workspace
        if hasattr(obj, 'workspace'):
            workspace = view.get_workspace()
            if obj.workspace != workspace:
                return False

        return self.has_permission(request, view)
