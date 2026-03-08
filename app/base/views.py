import logging
from typing import TYPE_CHECKING, Any

from django.contrib.messages import get_messages
from django.http import HttpRequest, HttpResponse
from django.utils.functional import Promise
from rest_framework import status
from rest_framework.response import Response

from base.serializers import ErrorSerializer

if TYPE_CHECKING:
    pass


logger = logging.getLogger('django.request')


class BaseAPIError(Exception):
    pass


class BaseApiResponseMixin:
    def finalize_response(
        self, request: HttpRequest, response: HttpResponse, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        response = super().finalize_response(request, response, *args, **kwargs)  # type: ignore

        if response.status_code >= status.HTTP_400_BAD_REQUEST:
            self._handle_error_response(response)

        self._add_notifications(request, response)

        return response

    def _handle_error_response(self, response: HttpResponse) -> None:
        if isinstance(response.data, dict):
            self._handle_dict_error_response(response)
        else:
            response.data = {'status': False, 'data': str(response.data)}

    def _handle_dict_error_response(self, response: HttpResponse) -> None:
        if 'error_code' in response.data:
            # Already in expected format
            return
        if 'detail' in response.data and len(response.data) == 1:
            response.data = {'status': False, 'error_message': response.data['detail']}
        else:
            self._handle_complex_error_response(response)

    def _handle_complex_error_response(self, response: HttpResponse) -> None:
        data = response.data
        response.data = {'status': False}

        if 'error_message' in data:
            response.data['error_message'] = data.pop('error_message')
        if data:
            response.data['field_errors'] = data

    def _add_notifications(self, request: HttpRequest, response: HttpResponse) -> None:
        messages_context = []
        for message in get_messages(request):
            messages_context.append({'message': message.message, 'tags': message.tags})
        if messages_context:
            response.data['$notifications'] = messages_context

    def get_error_response(
        self,
        *,
        error_message: str | Promise,
        error_code: int,
        http_status: int = status.HTTP_400_BAD_REQUEST,
        field_errors: dict | None = None,
        data: dict | None = None,
    ) -> Response:
        payload = {
            "status": False,
            "error_code": int(error_code),
            "error_message": str(error_message),
            "field_errors": field_errors,
            "data": data,
        }
        serializer = ErrorSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=http_status)
