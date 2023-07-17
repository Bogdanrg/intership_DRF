from rest_framework import viewsets, mixins, permissions, response, status
from src.base.permissions import ActionPermissionMixin, IsAdminOrAnalyst
from .models import Portfolio, PortfolioUserPromotion
from .serializers import PortfolioSerializer
from ..profiles.models import TradingUser


class UserPortfolioViewSet(ActionPermissionMixin,
                           viewsets.GenericViewSet,
                           mixins.ListModelMixin):

    serializer_class = PortfolioSerializer
    permission_classes_by_action = {
        'list': [permissions.IsAuthenticated]
    }

    def get_queryset(self):
        portfolio = Portfolio.objects.get(user=self.request.user)
        return PortfolioUserPromotion.objects.filter(portfolio=portfolio)


class AnyUserPortfolioViewSet(ActionPermissionMixin,
                              viewsets.GenericViewSet,
                              mixins.RetrieveModelMixin):
    lookup_field = 'pk'
    permission_classes_by_action = {
        'retrieve': [IsAdminOrAnalyst]
    }
    serializer_class = PortfolioSerializer

    def get_queryset(self):
        user = TradingUser.objects.get(pk=self.kwargs.get('pk'))
        portfolio = Portfolio.objects.get(user=user)
        return PortfolioUserPromotion.objects.filter(portfolio=portfolio)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
