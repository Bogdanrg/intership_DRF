import json
import os

import jwt
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from dotenv import load_dotenv

from src.profiles.models import TradingUser

SAFE_PATHS = [
    "/api/auth-custom/",
    "/admin/login/",
    "/api/auth-custom/refresh/",
    "/admin/",
    "/admin/orders/order/",
]

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")


def create_response(code, message):
    try:
        data = {"data": message, "code": int(code)}
        return data
    except Exception as creation_error:
        print("Can't create response", creation_error)


class CustomMiddleware(MiddlewareMixin):
    def process_request(self, request):
        jwt_token = request.headers.get("authorization", None)

        if jwt_token:
            try:
                payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=["HS256"])
                username = payload["username"]
                print(username)
                request.user = TradingUser.objects.get(username=username)
                setattr(request, "_dont_enforce_csrf_checks", True)
                return None
            except jwt.ExpiredSignatureError:
                response = create_response(
                    4001, {"message": "Authentication token has expired"}
                )
                return HttpResponse(json.dumps(response), status=401)
            except (jwt.DecodeError, jwt.InvalidTokenError):
                response = create_response(
                    4001,
                    {"message": "Authorization has failed, Please send valid token."},
                )
                return HttpResponse(json.dumps(response), status=401)
        else:
            if request.path in SAFE_PATHS:
                return None
            response = create_response(
                4001,
                {
                    "message": "Authorization not found, Please send valid token in headers"
                },
            )
            return HttpResponse(json.dumps(response), status=401)
