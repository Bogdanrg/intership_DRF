from django.db.models import QuerySet
from django.utils.decorators import method_decorator
from rest_framework import mixins, permissions, response, status, viewsets
from django.db import transaction

from src.base.permissions import ActionPermissionMixin, IsAdmin, IsAdminOrAnalyst
from src.base.serializers import ActionSerializerMixin

from .models import Order
from .serializers import CreateOrderSerializer, OrderListSerializer, OrderSerializer
from .services import OrderBuyService, OrderSellService


@method_decorator(transaction.atomic, name='create')
class UsersOrderListViewSet(
    ActionSerializerMixin,
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
):
    permission_classes = [permissions.IsAuthenticated]
    serializer_classes_by_action = {
        "list": OrderListSerializer,
        "create": CreateOrderSerializer,
    }

    def get_queryset(self) -> QuerySet:
        return self.request.user.orders.filter(action='purchase').select_related("promotion")

    def create(self, request, *args, **kwargs) -> response.Response:
        order_service = OrderBuyService(request)
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


@method_decorator(transaction.atomic, name='create')
class OrderSellListViewSet(ActionSerializerMixin,
                           viewsets.GenericViewSet,
                           mixins.ListModelMixin,
                           mixins.CreateModelMixin
                           ):
    permission_classes = [permissions.IsAuthenticated]
    serializer_classes_by_action = {
        "list": OrderListSerializer,
        "create": CreateOrderSerializer,
    }

    def get_queryset(self) -> QuerySet:
        return self.request.user.orders.filter(action='sale').select_related("promotion")

    def create(self, request, *args, **kwargs) -> response.Response:
        order_service = OrderSellService(request)
        if order_service.in_presence(request.data):
            data = order_service.create_order(request.data)
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            order_service.increase_user_balance(data)
            order_service.update_portfolio(request)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response("You don't have enough promotions", status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)


class UsersTransactionsViewSet(viewsets.GenericViewSet,
                               mixins.RetrieveModelMixin):
    lookup_field = 'pk'
    permission_classes = [IsAdminOrAnalyst]
    serializer_class = OrderListSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.kwargs.get('pk'))

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
