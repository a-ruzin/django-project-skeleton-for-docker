from core.api.v1.serializers.base_model_serializer import BaseModelSerializer
from core.models import Thing


class ThingSerializer(BaseModelSerializer):
    class Meta:
        model = Thing
        fields = ['id', 'payload']
        read_only_fields = ['created_at', 'updated_at']
