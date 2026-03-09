from django_filters import rest_framework as dj_filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from core.api.v1.mixins import CoreApiResponseMixin, WorkspaceScopedViewSetMixin
from core.api.v1.permissions import HasWorkspaceAccess
from core.api.v1.serializers.thing import ThingSerializer
from core.models import Thing


class ThingsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ThingsViewSet(WorkspaceScopedViewSetMixin, CoreApiResponseMixin, ModelViewSet):
    """
    ViewSet для работы с thing в рамках конкретного workspace.
    URL: /api/v1/ws/<workspace_slug>/things/

    Доступ: все пользователи с доступом к workspace могут работать с thing.
    Для ограничения прав используйте required_workspace_roles.
    """
    queryset = Thing.objects.all()
    serializer_class = ThingSerializer
    permission_classes = (IsAuthenticated, HasWorkspaceAccess)
    filter_backends = [filters.SearchFilter, dj_filters.DjangoFilterBackend]
    pagination_class = ThingsPagination

    @swagger_auto_schema(
        operation_summary="List things",
        operation_description="Возвращает список things для указанного workspace",
        responses={200: ThingSerializer(many=True)},
        tags=["things"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Get thing",
        operation_description="Возвращает thing по ID",
        responses={
            status.HTTP_200_OK: ThingSerializer,
            status.HTTP_404_NOT_FOUND: "Not found",
        },
        tags=["things"],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create thing",
        operation_description="Создаёт новый thing в workspace",
        request_body=ThingSerializer,
        responses={
            status.HTTP_201_CREATED: ThingSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad request",
        },
        tags=["things"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update thing",
        operation_description="Обновляет thing",
        request_body=ThingSerializer,
        responses={
            status.HTTP_200_OK: ThingSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad request",
            status.HTTP_404_NOT_FOUND: "Not found",
        },
        tags=["things"],
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial update thing",
        operation_description="Частично обновляет thing",
        request_body=ThingSerializer,
        responses={
            status.HTTP_200_OK: ThingSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad request",
            status.HTTP_404_NOT_FOUND: "Not found",
        },
        tags=["things"],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete thing",
        operation_description="Удаляет thing",
        responses={
            status.HTTP_204_NO_CONTENT: "Deleted",
            status.HTTP_404_NOT_FOUND: "Not found",
        },
        tags=["things"],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
