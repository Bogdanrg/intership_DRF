from django.db import transaction
from django.utils.decorators import method_decorator
from rest_framework import mixins, permissions, response, status, viewsets

from src.base.mixins import ActionPermissionMixin, ActionSerializerMixin
from src.base.permissions import IsAdmin, IsAdminOrAnalyst, IsOwnerOrAdminOrAnalyst

from .models import Order
from .serializers import CreateOrderSerializer, OrderListSerializer, OrderSerializer
from .services import OrderBuyService, OrderSellService


@method_decorator(transaction.atomic, name="create")
class OrderCRUDViewSet(
    ActionSerializerMixin,
    ActionPermissionMixin,
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    permission_classes_by_action = {
        "create": (permissions.IsAuthenticated,),
        "retrieve": (IsOwnerOrAdminOrAnalyst,),
        "update": (IsAdmin,),
        "destroy": (IsAdmin,),
    }
    serializer_classes_by_action = {
        "retrieve": OrderSerializer,
        "create": CreateOrderSerializer,
        "update": OrderSerializer,
        "destroy": OrderSerializer,
    }
    queryset = Order.objects.all().select_related("promotion")

    def create(self, request, *args, **kwargs) -> response.Response:
        if request.data.get("action") == "purchase":
            order_service = OrderBuyService()
            data = order_service.create_order(request)
            if not data:
                return response.Response(
                    "You don't have enough money or something went wrong",
                    status.HTTP_406_NOT_ACCEPTABLE,
                )
            data = self.init_data(data)
            return response.Response(data, status=status.HTTP_200_OK)
        if request.data.get("action") == "sale":
            sell_order = OrderSellService()
            data = sell_order.create_order(request)
            if not data:
                return response.Response(
                    "You don't have enough promotions or something went wrong",
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
            data = self.init_data(data)
            return response.Response(data, status=status.HTTP_200_OK)
        else:
            return response.Response(
                "Not valid action", status=status.HTTP_406_NOT_ACCEPTABLE
            )

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)

    def init_data(self, data: dict) -> dict:
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return serializer.data


class UsersTransactionsViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    lookup_field = "pk"
    permission_classes = (IsAdminOrAnalyst,)
    serializer_class = OrderListSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.kwargs.get("pk"))

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
