from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from src.base.permissions import ActionPermissionMixin, IsAdmin, IsOwnerOrAdmin

from .models import TradingUser
from .serializers import UserProfileSerializer


class UserProfileViewSet(
    ActionPermissionMixin,
    GenericViewSet,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    lookup_field = "pk"
    serializer_class = UserProfileSerializer
    permission_classes_by_action = {"retrieve": [IsOwnerOrAdmin], "update": [IsAdmin]}

    def get_queryset(self):
        return TradingUser.objects.filter(pk=self.kwargs.get("pk"))
