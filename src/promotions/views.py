from src.base.classes import MixedPermissionListGenericViewSet,\
    MixedPermissionCRUD
from src.base.permissions import IsAdmin

from rest_framework import permissions
from .models import Promotion
from .serializers import PromotionSerializer, PromotionListSerializer


class ListPromotionViewSet(MixedPermissionListGenericViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionListSerializer
    permission_classes = [permissions.AllowAny]


class CreateRetrieveUpdateDestroyViewSet(MixedPermissionCRUD):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes_by_action = {
        'retrieve': [permissions.AllowAny],
        'update': [IsAdmin],
        'destroy': [IsAdmin],
        'create': [IsAdmin]
    }
