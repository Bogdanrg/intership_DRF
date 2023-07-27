from rest_framework import permissions, response, status, viewsets
from rest_framework.mixins import CreateModelMixin

from src.base.mixins import ActionPermissionMixin, ActionSerializerMixin

from .serializers import CreateAutoOrderSerializer
from .services import AutoOrderBuyService


class AutoOrderViewSet(
    ActionSerializerMixin,
    ActionPermissionMixin,
    viewsets.GenericViewSet,
    CreateModelMixin,
):
    permission_classes_by_action = {"create": (permissions.IsAuthenticated,)}
    serializer_classes_by_action = {"create": CreateAutoOrderSerializer}

    def create(self, request, *args, **kwargs) -> response.Response:
        if request.data.get("action") == "purchase":
            auto_order_service = AutoOrderBuyService()
            data = auto_order_service.create_order(request)
            data = self.init_data(data)
            return response.Response(data, status=status.HTTP_200_OK)

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)

    def init_data(self, data: dict) -> dict:
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return serializer.data
