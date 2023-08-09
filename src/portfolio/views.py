from django.db.models import QuerySet
from rest_framework import mixins, permissions, response, status, viewsets
from rest_framework.request import Request

from src.base.mixins import ActionPermissionMixin
from src.base.permissions import IsAdminOrAnalyst

from ..profiles.models import TradingUser
from .models import Portfolio, PortfolioUserPromotion
from .serializers import PortfolioSerializer


class UserPortfolioViewSet(
    ActionPermissionMixin, viewsets.GenericViewSet, mixins.ListModelMixin
):
    serializer_class = PortfolioSerializer
    permission_classes_by_action = {"list": (permissions.IsAuthenticated,)}

    def get_queryset(self) -> QuerySet:
        portfolio = Portfolio.objects.get(user=self.request.user)
        return PortfolioUserPromotion.objects.filter(portfolio=portfolio)


class AnyUserPortfolioViewSet(
    ActionPermissionMixin, viewsets.GenericViewSet, mixins.RetrieveModelMixin
):
    lookup_field = "pk"
    permission_classes_by_action = {"retrieve": (IsAdminOrAnalyst,)}
    serializer_class = PortfolioSerializer

    def get_queryset(self) -> QuerySet:
        user = TradingUser.objects.get(pk=self.kwargs.get("pk"))
        portfolio = Portfolio.objects.get(user=user)
        return PortfolioUserPromotion.objects.filter(portfolio=portfolio)

    def retrieve(
        self, request: Request, *args: tuple, **kwargs: dict
    ) -> response.Response:
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
