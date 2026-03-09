from typing import Any

from django.http import HttpRequest
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from base.serializers import ErrorSerializer
from core.api.v1.mixins import CoreApiResponseMixin
from core.api.v1.serializers.user import UserSerializer


class UserInfoView(CoreApiResponseMixin, APIView):
    http_method_names = ['get']
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_summary='Get user info',
        responses={
            200: UserSerializer(),
            401: ErrorSerializer(),
        }
    )
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        user_data = UserSerializer(instance=request.user).data
        return Response(user_data)
