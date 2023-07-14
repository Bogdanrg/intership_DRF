from src.base.permissions import IsAdmin, ActionPermissionMixin
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework import permissions
from .models import Promotion
from .serializers import PromotionSerializer, PromotionListSerializer


class CreateListPromotionViewSet(ActionPermissionMixin,
                                 mixins.ListModelMixin,
                                 mixins.CreateModelMixin,
                                 GenericViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionListSerializer
    permission_classes_by_action = {
        'list': [permissions.IsAuthenticated],
        'create': [IsAdmin]
    }


class RetrieveUpdateDestroyViewSet(ActionPermissionMixin,
                                   GenericViewSet,
                                   mixins.RetrieveModelMixin,
                                   mixins.UpdateModelMixin,
                                   mixins.DestroyModelMixin):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes_by_action = {
        'retrieve': [permissions.IsAuthenticated],
        'update': [IsAdmin],
        'destroy': [IsAdmin],
    }
