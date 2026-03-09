from core.api.v1.serializers.base_model_serializer import BaseModelSerializer
from core.models import Workspace


class WorkspaceSerializerForCreate(BaseModelSerializer):
    class Meta:
        model = Workspace
        fields = ['id', 'name', 'slug']
        read_only_fields = ['id']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
