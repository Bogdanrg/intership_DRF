from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet

from src.base.permissions import ActionPermissionMixin, IsAdmin
from src.base.serializers import ActionSerializerMixin

from .models import Promotion
from .serializers import PromotionListSerializer, PromotionSerializer


class CreateListPromotionViewSet(
    ActionPermissionMixin,
    ActionSerializerMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = Promotion.objects.all()
    permission_classes_by_action = {
        "list": [permissions.IsAuthenticated],
        "create": [IsAdmin],
    }
    serializer_classes_by_action = {
        "list": PromotionListSerializer,
        "create": PromotionSerializer,
    }


class RetrieveUpdateDestroyViewSet(
    ActionPermissionMixin,
    GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes_by_action = {
        "retrieve": [permissions.IsAuthenticated],
        "update": [IsAdmin],
        "destroy": [IsAdmin],
    }
