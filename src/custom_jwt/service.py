import datetime
import os

import jwt
from django.contrib.auth.hashers import check_password
from dotenv import load_dotenv

from src.profiles.models import TradingUser

from .serializers import JWTPairSerializer, UserCredentialsSerializer

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")


class JWTAuthService:

    @staticmethod
    def check_credentials(data: dict) -> bool:
        serializer = UserCredentialsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = TradingUser.objects.get(username=serializer.data.get("username"))
        if not user:
            return False
        if check_password(serializer.data.get("password"), user.password):
            return True
        return False

    @staticmethod
    def create_jwt_pair(data: dict) -> dict:
        serializer = UserCredentialsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        access_token = jwt.encode(
            {
                "username": serializer.data.get('username'),
                "type": "access_token",
                "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                        + datetime.timedelta(minutes=5),
            },
            SECRET_KEY,
            algorithm="HS256"
        )
        refresh_token = jwt.encode(
            {
                "username": serializer.data.get('username'),
                "type": "refresh_token",
                "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                        + datetime.timedelta(hours=24),
            },
            SECRET_KEY,
            algorithm="HS256"
        )
        tokens = {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        serializer = JWTPairSerializer(tokens)
        return serializer.data

    @staticmethod
    def encode_refresh(decoded_refresh_token) -> dict:
        access_token = jwt.encode(
            {
                "username": decoded_refresh_token.get('username'),
                "type": "access_token",
                "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                        + datetime.timedelta(minutes=5),
            },
            SECRET_KEY,
            algorithm="HS256",
        )
        tokens = {
            "access_token": access_token,
            "refresh_token": jwt.encode(decoded_refresh_token, SECRET_KEY, algorithm="HS256")
        }
        serializer = JWTPairSerializer(tokens)
        return serializer.data

    @staticmethod
    def decode_refresh_token(data: dict) -> dict | bool:
        try:
            serializer = JWTPairSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            return jwt.decode(serializer.data.get('refresh_token'), SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return False
        except (jwt.DecodeError, jwt.InvalidTokenError):
            return False
