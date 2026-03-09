from django.db.models import Case, When, Value, IntegerField
from django_filters import rest_framework as dj_filters
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from base.serializers import ErrorSerializer
from core.api.errors import ErrorCode
from core.api.v1.mixins import CoreApiResponseMixin
from core.api.v1.serializers.workspace import (
    WorkspaceSerializer,
    WorkspaceSerializerForCreate,
    WorkspaceSerializerForUpdate,
)
from core.models import Sentinel
from core.models.querysets import WorkspaceQuerySet


class WorkspaceViewSet(
    CoreApiResponseMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Sentinel.objects.all()
    serializer_class = WorkspaceSerializer
    permission_classes = (IsAuthenticated,)
    page_size_query_param = 'page_size'
    filter_backends = [filters.SearchFilter, dj_filters.DjangoFilterBackend]
    search_fields = ['name', 'slug']

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            return [IsAuthenticated(), IsWorkspaceOwner()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create':
            return WorkspaceSerializerForCreate
        if self.action in ('update', 'partial_update'):
            return WorkspaceSerializerForUpdate
        return WorkspaceSerializer

    def get_queryset(self) -> WorkspaceQuerySet:
        return (
            super()
            .get_queryset()
            .accessible_to_user(user=self.request.user)
            .annotate(
                is_owner=Case(
                    When(owner=self.request.user, then=Value(0)),
                    default=Value(1),
                    output_field=IntegerField(),
                )
            )
            .order_by('is_owner', 'name')
        )

    def _workspace_has_related_data(self, workspace: Sentinel) -> bool:
        """
        Проверяет, есть ли у workspace связанные данные через WorkspaceModel.
        Ищет все ForeignKey, указывающие на Workspace (кроме owner и user_roles).
        """
        for related in workspace._meta.related_objects:
            accessor_name = related.get_accessor_name()
            if accessor_name == 'user_roles':
                continue
            manager = getattr(workspace, accessor_name)
            if manager.exists():
                return True
        return False

    # ── List ─────────────────────────────────────────────────────

    @swagger_auto_schema(
        operation_summary="List workspaces",
        operation_description="Возвращает пространства, доступные текущему пользователю. "
                              "Собственные пространства идут первыми.",
        responses={200: WorkspaceSerializer(many=True)},
        tags=["workspaces"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # ── Retrieve ─────────────────────────────────────────────────

    @swagger_auto_schema(
        operation_summary="Get workspace",
        operation_description="Возвращает пространство по ID.",
        responses={
            200: WorkspaceSerializer,
            404: "Not found",
        },
        tags=["workspaces"],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # ── Create ───────────────────────────────────────────────────

    @swagger_auto_schema(
        operation_summary="Create workspace",
        operation_description="Создаёт новое пространство. Владельцем становится текущий пользователь.",
        request_body=WorkspaceSerializerForCreate,
        responses={
            201: WorkspaceSerializer,
            400: ErrorSerializer,
        },
        tags=["workspaces"],
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workspace = serializer.save()

        output_serializer = WorkspaceSerializer(workspace, context=self.get_serializer_context())
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    # ── Update ───────────────────────────────────────────────────

    @swagger_auto_schema(
        operation_summary="Update workspace",
        operation_description="Полностью обновляет пространство. Доступно только владельцу.",
        request_body=WorkspaceSerializerForUpdate,
        responses={
            200: WorkspaceSerializer,
            400: ErrorSerializer,
            403: "Forbidden — not owner",
            404: "Not found",
        },
        tags=["workspaces"],
    )
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        output_serializer = WorkspaceSerializer(instance, context=self.get_serializer_context())
        return Response(output_serializer.data)

    @swagger_auto_schema(
        operation_summary="Partial update workspace",
        operation_description="Частично обновляет пространство. Доступно только владельцу.",
        request_body=WorkspaceSerializerForUpdate,
        responses={
            200: WorkspaceSerializer,
            400: ErrorSerializer,
            403: "Forbidden — not owner",
            404: "Not found",
        },
        tags=["workspaces"],
    )
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        output_serializer = WorkspaceSerializer(instance, context=self.get_serializer_context())
        return Response(output_serializer.data)

    # ── Delete ───────────────────────────────────────────────────

    @swagger_auto_schema(
        operation_summary="Delete workspace",
        operation_description=(
                "Удаляет пространство. Доступно только владельцу. "
                "Если пространство содержит связанные данные — удаление невозможно."
        ),
        responses={
            204: "Deleted",
            403: "Forbidden — not owner",
            404: "Not found",
            409: openapi.Response(
                description="Workspace has related data",
                schema=ErrorSerializer,
            ),
        },
        tags=["workspaces"],
    )
    def destroy(self, request, *args, **kwargs):
        workspace = self.get_object()

        if self._workspace_has_related_data(workspace):
            return self.get_error_response_from_code(ErrorCode.WORKSPACE_NOT_EMPTY)

        workspace.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
