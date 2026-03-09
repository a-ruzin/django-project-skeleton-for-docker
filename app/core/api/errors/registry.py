from dataclasses import dataclass

from django.utils.functional import Promise
from django.utils.translation import gettext_lazy as _
from rest_framework import status

from .codes import ErrorCode


@dataclass(frozen=True)
class ErrorSpec:
    http_status: int
    message: str | Promise


ERRORS: dict[ErrorCode, ErrorSpec] = {
    ErrorCode.NOT_AUTHORIZED: ErrorSpec(
        http_status=status.HTTP_401_UNAUTHORIZED,
        message=_("Пользователь не авторизован"),
    ),
    ErrorCode.WRONG_PASSWORD: ErrorSpec(
        http_status=status.HTTP_400_BAD_REQUEST,
        message=_("Неверный пароль"),
    ),
    ErrorCode.AUTHENTICATED_CANNOT_REGISTER: ErrorSpec(
        http_status=status.HTTP_403_FORBIDDEN,
        message=_("Зарегистрированные пользователи не могут создавать новые аккаунты"),
    ),
    ErrorCode.WRONG_CONFIRMATION_CODE: ErrorSpec(
        http_status=status.HTTP_400_BAD_REQUEST,
        message=_("Неверный код подтверждения"),
    ),
    ErrorCode.EXPIRED_REGISTRATION_REQUEST: ErrorSpec(
        http_status=status.HTTP_400_BAD_REQUEST,
        message=_("Неверная или просроченная заявка на регистрацию"),
    ),
    ErrorCode.WORKSPACE_NOT_EMPTY: ErrorSpec(
        http_status=status.HTTP_409_CONFLICT,
        message=_("Невозможно удалить пространство, содержащее данные"),
    ),
    ErrorCode.WORKSPACE_ACCESS_DENIED: ErrorSpec(
        http_status=status.HTTP_403_FORBIDDEN,
        message=_("У вас нет доступа к этому пространству"),
    ),
    ErrorCode.WORKSPACE_INSUFFICIENT_PERMISSIONS: ErrorSpec(
        http_status=status.HTTP_403_FORBIDDEN,
        message=_("У вас недостаточно прав для выполнения этого действия"),
    ),
    ErrorCode.UNKNOWN: ErrorSpec(
        http_status=status.HTTP_400_BAD_REQUEST,
        message=_("Произошла неизвестная ошибка"),
    ),
}
