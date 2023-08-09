import datetime

import jwt
from django.conf import settings
from django.contrib.auth.hashers import check_password

from src.profiles.models import TradingUser

from .serializers import JWTPairSerializer, LoginUserSerializer

JWT_SECRET_KEY = settings.JWT_SECRET_KEY


class JWTAuthService:
    @staticmethod
    def check_credentials(data: dict) -> bool:
        serializer = LoginUserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        try:
            user = TradingUser.objects.get(username=serializer.data.get("username"))
        except TradingUser.DoesNotExist:
            return False
        if check_password(serializer.data.get("password"), user.password):
            return True
        return False

    @staticmethod
    def create_jwt_pair(data: dict) -> dict:
        serializer = LoginUserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        access_token = jwt.encode(
            {
                "username": serializer.data.get("username"),
                "type": "access_token",
                "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                + datetime.timedelta(minutes=5),
            },
            JWT_SECRET_KEY,
            algorithm="HS256",
        )
        refresh_token = jwt.encode(
            {
                "username": serializer.data.get("username"),
                "type": "refresh_token",
                "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                + datetime.timedelta(hours=24),
            },
            JWT_SECRET_KEY,
            algorithm="HS256",
        )
        tokens = {"access_token": access_token, "refresh_token": refresh_token}
        serializer = JWTPairSerializer(tokens)
        return serializer.data

    @staticmethod
    def encode_refresh(decoded_refresh_token: dict) -> dict:
        access_token = jwt.encode(
            {
                "username": decoded_refresh_token.get("username"),
                "type": "access_token",
                "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                + datetime.timedelta(minutes=5),
            },
            JWT_SECRET_KEY,
            algorithm="HS256",
        )
        tokens = {
            "access_token": access_token,
            "refresh_token": jwt.encode(
                decoded_refresh_token, JWT_SECRET_KEY, algorithm="HS256"
            ),
        }
        serializer = JWTPairSerializer(tokens)
        return serializer.data

    @staticmethod
    def decode_refresh_token(data: dict) -> dict | bool:
        try:
            serializer = JWTPairSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            return jwt.decode(
                serializer.data.get("refresh_token"),
                JWT_SECRET_KEY,
                algorithms=["HS256"],
            )
        except jwt.ExpiredSignatureError:
            return False
        except (jwt.DecodeError, jwt.InvalidTokenError):
            return False
