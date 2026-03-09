from core.api.v1.serializers.base_model_serializer import BaseModelSerializer
from core.models import UserRegistrationRequest


class UserRegistrationRequestSerializer(BaseModelSerializer):
    class Meta:
        model = UserRegistrationRequest
        fields = ['id', 'phone']
