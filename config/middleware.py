import json
import os
import re
import jwt
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from dotenv import load_dotenv

from src.profiles.models import TradingUser

AUTH_PATHS = [
    '/api/auth-custom/',
    '/api/auth-custom/registration/',
    '/api/auth-custom/refresh/',
    re.search('/api/auth-custom/verification/\S+',
              '/api/auth-custom/verification/<username>'),
    '/api/auth-custom/password_reset/',
    '/api/auth-custom/password_reset/confirm/'
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
        jwt_token = request.headers.get("JWT", None)

        if jwt_token:
            try:
                payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=["HS256"])
                username = payload["username"]
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
            if re.search(r'/admin\S+', request.path) or request.path in AUTH_PATHS:
                return None
            response = create_response(
                4001,
                {
                    "message": "Authorization not found, Please send valid token in headers"
                },
            )
            return HttpResponse(json.dumps(response), status=401)
