from django.db.models import QuerySet
from rest_framework.response import Response

from rest_framework import permissions, status, viewsets, mixins
from .serializers import OrderListSerializer, OrderSerializer, CreateOrderSerializer
from .models import Order
from src.base.permissions import IsAdminOrAnalyst, IsAdmin, ActionPermissionMixin
from .services import order_service


class UsersOrderListCreateViewSet(viewsets.GenericViewSet,
                                  mixins.ListModelMixin,
                                  mixins.CreateModelMixin):

    serializer_class = OrderListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        return self.request.user.orders.all().select_related('promotion')

    def create(self, request, *args, **kwargs) -> Response:
        data = order_service.create_order(request.data, kwargs.get('pk'))
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)


class OrderViewSet(ActionPermissionMixin,
                   viewsets.GenericViewSet,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin):

    queryset = Order.objects.all().select_related('promotion')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    permission_classes_by_action = {
        'retrieve': [IsAdminOrAnalyst],
        'update': [IsAdmin],
        'destroy': [IsAdmin],
    }
