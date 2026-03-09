from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from core.api.v1.mixins import CoreApiResponseMixin
from core.api.v1.serializers.sentinel import SentinelSerializer
from core.models import Sentinel


class SentinelsViewSet(CoreApiResponseMixin, ModelViewSet):
    """
    ViewSet для работы с sentinel в рамках конкретного workspace.
    URL: /api/v1/ws/<workspace_slug>/sentinels/

    Доступ: все пользователи с доступом к workspace могут работать с sentinel.
    Для ограничения прав используйте required_workspace_roles.
    """
    queryset = Sentinel.objects.all()
    serializer_class = SentinelSerializer
    permission_classes = (IsAuthenticated,)
