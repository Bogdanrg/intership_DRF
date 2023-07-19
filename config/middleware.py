from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework.request import Request

from .services import AuthMiddlewareService


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request: Request) -> None | HttpResponse:
        auth_service = AuthMiddlewareService()
        jwt_token = auth_service.get_token(request)
        if jwt_token:
            payload = auth_service.get_payload(jwt_token)
            if isinstance(payload, dict):
                auth_service.authenticate_user(request, payload)
                return None
            return payload
        else:
            return auth_service.is_safe_path(request)
