from core.api.v1.serializers.base_model_serializer import BaseModelSerializer
from core.models import User


class UserSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone', 'email']
