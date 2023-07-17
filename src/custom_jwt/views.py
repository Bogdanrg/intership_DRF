from rest_framework import response, status, viewsets, permissions, mixins
from rest_framework.views import APIView
from .serializers import RegistrationUserSerializer, ChangePasswordSerializer
from .services import JWTAuthService
from .tasks import send_notification_mail
from ..profiles.models import TradingUser
from src.portfolio.models import Portfolio


class CreateTokenPairAPIView(APIView):
    def post(self, request):
        jwt_service = JWTAuthService()
        access = jwt_service.check_credentials(request.data)
        if access:
            return response.Response(jwt_service.create_jwt_pair(request.data))
        return response.Response(
            "Wrong credentials", status=status.HTTP_400_BAD_REQUEST
        )


class RefreshAccessToken(APIView):
    def post(self, request):
        jwt_service = JWTAuthService()
        refresh_token = jwt_service.decode_refresh_token(request.data)
        if refresh_token:
            data = jwt_service.encode_refresh(refresh_token)
            return response.Response(data, status=status.HTTP_200_OK)
        return response.Response(
            "Wrong refresh token", status=status.HTTP_400_BAD_REQUEST
        )


class RegistrationUserAPIView(APIView):

    def post(self, request):
        serializer = RegistrationUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        email = serializer.data.get('email')
        send_notification_mail.delay(email, user.username)
        return response.Response("Verify your email", status=status.HTTP_200_OK)


class ActivateUserAPIView(APIView):
    def get(self, request, username, *args, **kwargs):
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
            return response.Response("Your account has been confirmed", status=status.HTTP_200_OK)


class ChangePasswordViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not user.check_password(serializer.data.get('old_password')):
            return response.Response("Wrong old password")
        user.set_password(serializer.data.get('new_password'))
        user.save()
        return response.Response("Password has been changed", status=status.HTTP_200_OK)
