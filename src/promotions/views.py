from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet

from src.base.mixins import ActionPermissionMixin, ActionSerializerMixin
from src.base.permissions import IsAdmin

from .models import Promotion
from .serializers import PromotionListSerializer, PromotionSerializer


class PromotionListCRUDViewSet(
    ActionPermissionMixin,
    ActionSerializerMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Promotion.objects.all()
    permission_classes_by_action = {
        "list": (permissions.IsAuthenticated,),
        "create": (IsAdmin,),
        "retrieve": (permissions.IsAuthenticated,),
        "update": (IsAdmin,),
        "destroy": (IsAdmin,),
    }
    serializer_classes_by_action = {
        "list": PromotionListSerializer,
        "create": PromotionSerializer,
        "retrieve": PromotionSerializer,
        "update": PromotionSerializer,
        "destroy": PromotionSerializer,
    }
