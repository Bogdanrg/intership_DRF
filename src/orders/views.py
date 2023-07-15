from django.db.models import QuerySet
from django.utils.decorators import method_decorator
from rest_framework import mixins, permissions, response, status, viewsets
from django.db import transaction

from src.base.permissions import ActionPermissionMixin, IsAdmin, IsAdminOrAnalyst
from src.base.serializers import ActionSerializerMixin

from .models import Order
from .serializers import CreateOrderSerializer, OrderListSerializer, OrderSerializer
from .services import OrderCreationService


@method_decorator(transaction.atomic, name='create')
class UsersOrderListViewSet(
    ActionSerializerMixin,
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
):
    serializer_classes_by_action = {
        "list": OrderListSerializer,
        "create": CreateOrderSerializer,
    }

    def get_queryset(self) -> QuerySet:
        return self.request.user.orders.all().select_related("promotion")

    def create(self, request, *args, **kwargs) -> response.Response:
        order_service = OrderCreationService()
        affordable = order_service.is_affordable(request)
        if affordable:
            data = order_service.create_order(request)
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            order_service.reduce_user_balance(data)
            order_service.update_portfolio(data)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(
            "You don't have enough money or something went wrong",
            status.HTTP_406_NOT_ACCEPTABLE,
        )

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)


class OrderViewSet(
    ActionPermissionMixin,
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Order.objects.all().select_related("promotion")
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    permission_classes_by_action = {
        "retrieve": [IsAdminOrAnalyst],
        "update": [IsAdmin],
        "destroy": [IsAdmin]
    }
