import json
import os
import re

import jwt
from django.http import HttpResponse
from dotenv import load_dotenv
from rest_framework.request import Request

from src.profiles.models import TradingUser

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")

AUTH_PATHS = [
    "/api/auth-custom/",
    "/api/auth-custom/registration/",
    "/api/auth-custom/refresh/",
    "/api/auth-custom/password_reset/",
    "/api/auth-custom/password_reset/confirm/",
]


class AuthMiddlewareService:
    @staticmethod
    def create_response(code: int, message: dict) -> dict:
        try:
            data = {"data": message, "code": int(code)}
            return data
        except Exception as creation_error:
            print("Can't create response", creation_error)

    @staticmethod
    def authenticate_user(request: Request, payload) -> None:
        username = payload["username"]
        request.user = TradingUser.objects.get(username=username)
        setattr(request, "_dont_enforce_csrf_checks", True)

    @staticmethod
    def get_payload(jwt_token: str) -> dict | HttpResponse:
        try:
            payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            response = AuthMiddlewareService.create_response(
                4001, {"message": "Authentication token has expired"}
            )
            return HttpResponse(json.dumps(response), status=401)
        except (jwt.DecodeError, jwt.InvalidTokenError):
            response = AuthMiddlewareService.create_response(
                4001,
                {"message": "Authorization has failed, Please send valid token."},
            )
            return HttpResponse(json.dumps(response), status=401)

    @staticmethod
    def get_token(request: Request) -> str | None:
        return request.headers.get("JWT", None)

    @staticmethod
    def is_safe_path(request: Request) -> bool | HttpResponse:
        if (
            re.search(r"/admin\S+", request.path)
            or request.path in AUTH_PATHS
            or re.search("/api/auth-custom/verification\S+", request.path)
        ):
            return True
        response = AuthMiddlewareService.create_response(
            4001,
            {"message": "Authorization not found, Please send valid token in headers"},
        )
        return HttpResponse(json.dumps(response), status=401)
