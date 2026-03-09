from core.api.v1.serializers.base_model_serializer import BaseModelSerializer
from core.models import Workspace


class WorkspaceSerializer(BaseModelSerializer):
    class Meta:
        model = Workspace
        fields = ['id', 'name', 'slug', 'owner']
