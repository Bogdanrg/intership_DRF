from rest_framework import permissions, response, status, viewsets
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)

from src.base.mixins import ActionPermissionMixin, ActionSerializerMixin
from src.base.permissions import IsAdmin, IsOwnerOrAdminOrAnalyst

from .models import AutoOrder
from .serializers import AutoOrderSerializer, CreateAutoOrderSerializer
from .services import AutoOrderBuyService, AutoOrderSaleService


class AutoOrderViewSet(
    ActionSerializerMixin,
    ActionPermissionMixin,
    viewsets.GenericViewSet,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    queryset = AutoOrder.objects.all().select_related("promotion")

    permission_classes_by_action = {
        "create": (permissions.IsAuthenticated,),
        "update": (IsAdmin,),
        "retrieve": (IsOwnerOrAdminOrAnalyst,),
        "destroy": (IsAdmin,),
    }
    serializer_classes_by_action = {
        "create": CreateAutoOrderSerializer,
        "update": AutoOrderSerializer,
        "retrieve": AutoOrderSerializer,
    }

    def create(self, request, *args, **kwargs) -> response.Response:
        if request.data.get("action") == "purchase":
            auto_order_service = AutoOrderBuyService()
            data = auto_order_service.create_order(request)
            if not data:
                return response.Response(
                    "You don't have enough money or something went wrong",
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
            data = self.init_data(data)
            return response.Response(data, status=status.HTTP_200_OK)
        if request.data.get("action") == "sale":
            auto_order_service = AutoOrderSaleService()
            data = auto_order_service.create_order(request)
            if not data:
                return response.Response(
                    "You don't have enough promotions or something went wrong",
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
            data = self.init_data(data)
            return response.Response(data, status=status.HTTP_200_OK)

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)

    def init_data(self, data: dict) -> dict:
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return serializer.data
