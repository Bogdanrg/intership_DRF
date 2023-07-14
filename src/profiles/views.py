from src.base.permissions import IsOwnerOrAdmin, IsAdmin, ActionPermissionMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, permissions
from .serializers import UserProfileSerializer
from .models import TradingUser


class UserProfileViewSet(GenericViewSet,
                         ActionPermissionMixin,
                         mixins.UpdateModelMixin,
                         mixins.RetrieveModelMixin):

    lookup_field = 'pk'
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    permission_classes_by_action = {
        'retrieve': [IsOwnerOrAdmin],
        'update': [IsAdmin]
    }

    def get_queryset(self):
        return TradingUser.objects.filter(pk=self.kwargs.get('pk'))
