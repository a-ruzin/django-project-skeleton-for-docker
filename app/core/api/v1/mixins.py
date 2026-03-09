from __future__ import annotations

import logging
from typing import Optional

from django.shortcuts import get_object_or_404
from rest_framework.request import Request

from base.views import BaseApiResponseMixin
from core.api.errors import ERRORS, ErrorCode
from core.models import Workspace


class CoreApiResponseMixin(BaseApiResponseMixin):

    """
    Базовый миксин для всех вьюх API, который обеспечивает единообразный формат
    ответов и обработку ошибок. Все вьюхи API должны наследоваться от этого
    миксина, чтобы гарантировать согласованность в структуре ответов.
    """
    def get_error_response_from_code(
        self,
        code: ErrorCode,
        *,
        field_errors: dict | None = None,
        data: dict | None = None,
    ):
        spec = ERRORS.get(code)
        if spec is None:
            logging.error(f"Unknown error code: {code}")
            spec = ERRORS.get(ErrorCode.UNKNOWN)
        return self.get_error_response(
            error_message=spec.message,
            error_code=int(code),
            http_status=spec.http_status,
            field_errors=field_errors,
            data=data,
        )


class WorkspaceScopedViewSetMixin:
    """
    Миксин для ViewSet'ов, работающих в контексте конкретного workspace.

    Предоставляет:
    - Получение workspace по slug из URL
    - Проверку доступа пользователя к workspace
    - Автоматическую фильтрацию queryset по workspace
    - Автоматическую привязку создаваемых объектов к workspace

    Использование:
        class MyViewSet(WorkspaceScopedViewSetMixin, ModelViewSet):
            # ViewSet автоматически получит workspace из URL параметра
            # workspace_slug
            pass
    """

    # Имя поля в URL, содержащего slug workspace (можно переопределить)
    workspace_slug_url_kwarg = 'workspace_slug'

    # Имя поля модели, связывающего объект с workspace (можно переопределить)
    workspace_field_name = 'workspace'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cached_workspace: Optional[Workspace] = None

    def get_workspace(self) -> Workspace:
        """
        Получить workspace по slug из URL.
        Проверяет доступ текущего пользователя к workspace.
        Результат кешируется для повторных вызовов в рамках одного запроса.
        """
        if self._cached_workspace is not None:
            return self._cached_workspace

        workspace_slug = self.kwargs.get(self.workspace_slug_url_kwarg)
        if not workspace_slug:
            raise ValueError(
                f"URL должен содержать параметр '{self.workspace_slug_url_kwarg}'. "
                f"Проверьте настройку URL-маршрутов."
            )

        # Получаем workspace с проверкой доступа пользователя
        workspace = get_object_or_404(
            Workspace.objects.accessible_to_user(user=self.request.user),
            slug=workspace_slug
        )

        self._cached_workspace = workspace
        return workspace

    def get_queryset(self):
        """
        Фильтруем queryset только объектами текущего workspace.
        """
        queryset = super().get_queryset()
        workspace = self.get_workspace()

        # Фильтруем по workspace
        filter_kwargs = {self.workspace_field_name: workspace}
        return queryset.filter(**filter_kwargs)

    def perform_create(self, serializer):
        """
        При создании объекта автоматически привязываем его к текущему workspace.
        """
        workspace = self.get_workspace()
        save_kwargs = {self.workspace_field_name: workspace}
        serializer.save(**save_kwargs)

    def initial(self, request: Request, *args, **kwargs):
        """
        Переопределяем initial для сброса кеша workspace при новом запросе.
        """
        self._cached_workspace = None
        return super().initial(request, *args, **kwargs)
