from rest_framework import generics, mixins, permissions, response, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework.views import APIView

from src.portfolio.models import Portfolio

from ..profiles.models import TradingUser
from .serializers import (
    ChangePasswordSerializer,
    ConfirmResetPasswordSerializer,
    RegistrationUserSerializer,
    ResetPasswordSerializer,
)
from .services import JWTAuthService
from .tasks import send_change_password_mail, send_notification_mail


class CreateTokenPairAPIView(APIView):
    def post(self, request: Request) -> response.Response:
        jwt_service = JWTAuthService()
        access = jwt_service.check_credentials(request.data)
        if access:
            return response.Response(jwt_service.create_jwt_pair(request.data))
        return response.Response(
            "Wrong credentials", status=status.HTTP_400_BAD_REQUEST
        )


class RefreshAccessToken(APIView):
    def post(self, request: Request) -> response.Response:
        jwt_service = JWTAuthService()
        refresh_token = jwt_service.decode_refresh_token(request.data)
        if isinstance(refresh_token, dict):
            data = jwt_service.encode_refresh(refresh_token)
            return response.Response(data, status=status.HTTP_200_OK)
        return response.Response(
            "Wrong refresh token", status=status.HTTP_400_BAD_REQUEST
        )


class RegistrationUserAPIView(APIView):
    def post(self, request: Request) -> response.Response:
        serializer = RegistrationUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = TradingUser.objects.create_user(
            username=serializer.data.get("username"),
            password=serializer.data.get("password"),
            email=serializer.data.get("email"),
            is_active=False,
        )
        send_notification_mail.delay(user.email, user.username)
        return response.Response("Verify your email", status=status.HTTP_200_OK)


class ActivateUserAPIView(APIView):
    def get(
        self, request: Request, username: str, *args: tuple, **kwargs: dict
    ) -> response.Response:
        try:
            user = TradingUser.objects.get(username=username)
        except (TypeError, ValueError, OverflowError, TradingUser.DoesNotExist):
            user = None
        if user is None:
            return response.Response("Invalid link", status=status.HTTP_403_FORBIDDEN)
        else:
            user.is_active = True
            user.save()
            Portfolio.objects.create(user=user)
            return response.Response(
                "Your account has been confirmed", status=status.HTTP_200_OK
            )


class ChangePasswordViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(
        self, request: Request, *args: tuple, **kwargs: dict
    ) -> response.Response:
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not user.check_password(serializer.data.get("old_password")):
            return response.Response(
                "Wrong old password", status=status.HTTP_400_BAD_REQUEST
            )
        user.set_password(serializer.data.get("new_password"))
        user.save()
        return response.Response("Password has been changed", status=status.HTTP_200_OK)


class ResetPasswordAPIView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request: Request) -> response.Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = TradingUser.objects.get(username=serializer.data.get("username"))
        except TradingUser.DoesNotExist:
            return response.Response(
                "Invalid username", status=status.HTTP_400_BAD_REQUEST
            )
        token = Token.objects.create(user=user)
        send_change_password_mail.delay(
            serializer.data.get("email"),
            f"127.0.0.1:8000/api/auth-custom/reset_password/confirm/,"
            f"your token: {token.key}",
        )
        return response.Response("Check our email")


class ConfirmResetPasswordAPIView(generics.GenericAPIView):
    serializer_class = ConfirmResetPasswordSerializer

    def post(self, request: Request) -> response.Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = TradingUser.objects.get(username=serializer.data.get("username"))
        token, created = Token.objects.get_or_create(user=user)
        if not created:
            if not serializer.data.get("token") == token.key:
                token.delete()
                return response.Response("Wrong token")
            user.set_password(serializer.data.get("password"))
            user.save()
            token.delete()
            return response.Response("Password has been changed")
        return response.Response("Access denied")
