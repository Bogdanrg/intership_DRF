from django.db.models import QuerySet

from src.base.classes import List
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import OrderListSerializer, OrderSerializer
from .models import Order
from src.base.permissions import IsAdminOrAnalyst, IsAdmin


class UsersOrderListViewSet(List):
    serializer_class = OrderListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        return self.request.user.orders.all().select_related('promotion')


class OrderViewSet(viewsets.GenericViewSet):
    queryset = Order.objects.all().select_related('promotion')
    serializer_class = OrderSerializer
    permissions_classes_by_action = {
        'retrieve': [IsAdminOrAnalyst],
        'update': [IsAdmin],
        'destroy': [IsAdmin]
    }
