from django.utils.deprecation import MiddlewareMixin

from .services import AuthMiddlewareService


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_service = AuthMiddlewareService()
        jwt_token = auth_service.get_token(request)
        if jwt_token:
            payload = auth_service.get_payload(jwt_token)
            if isinstance(payload, dict):
                auth_service.authenticate_user(request, payload)
                return None
            return payload
        else:
            auth_service.is_safe_path(request)
