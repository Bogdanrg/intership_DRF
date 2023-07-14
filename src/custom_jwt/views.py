from rest_framework import response, status
from rest_framework.views import APIView

from .service import JWTAuthService


class CreateTokePairAPIView(APIView):
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
