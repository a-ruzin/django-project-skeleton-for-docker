from core.api.v1.serializers.base_model_serializer import BaseModelSerializer
from core.models import Sentinel


class SentinelSerializer(BaseModelSerializer):
    class Meta:
        model = Sentinel
        fields = ['id', 'payload']
