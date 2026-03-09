import json

from django.conf import settings
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.v1.mixins import CoreApiResponseMixin


class VersionView(CoreApiResponseMixin, APIView):
    def get(self, request: HttpRequest) -> Response:
        try:
            version_info = json.load(open(settings.VERSION_FILE, 'r'))
        except (json.JSONDecodeError, FileNotFoundError):
            return Response({'detail': 'version is unknown'}, status=501)

        return Response(version_info)
