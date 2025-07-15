import logging
from typing import TYPE_CHECKING, Any

from django.contrib.messages import get_messages
from django.http import HttpRequest, HttpResponse
from rest_framework import status
from rest_framework.exceptions import APIException

if TYPE_CHECKING:
    pass


logger = logging.getLogger('django.request')


class BaseAPIError(APIException):
    pass


class BaseApiResponseMixin:
    def finalize_response(
        self, request: HttpRequest, response: HttpResponse, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        response = super().finalize_response(request, response, *args, **kwargs)  # type: ignore

        if response.status_code < status.HTTP_400_BAD_REQUEST:
            self._handle_successful_response(response)
        else:
            self._handle_error_response(response)

        self._add_notifications(request, response)

        return response

    def _handle_successful_response(self, response: HttpResponse) -> None:
        if hasattr(response, 'data'):
            response.data = {'status': True, 'data': response.data}

    def _handle_error_response(self, response: HttpResponse) -> None:
        if isinstance(response.data, dict):
            self._handle_dict_error_response(response)
        else:
            response.data = {'status': False, 'data': str(response.data)}

    def _handle_dict_error_response(self, response: HttpResponse) -> None:
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
            response.data['form_errors'] = data

    def _add_notifications(self, request: HttpRequest, response: HttpResponse) -> None:
        messages_context = []
        for message in get_messages(request):
            messages_context.append({'message': message.message, 'tags': message.tags})
        if messages_context:
            response.data['notifications'] = messages_context
