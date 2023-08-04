from rest_framework import mixins, permissions, response, status
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet

from src.base.mixins import ActionPermissionMixin
from src.base.permissions import IsAdmin, IsOwnerOrAdmin
from src.promotions.models import Promotion
from src.promotions.serializers import PromotionListSerializer

from .models import PromotionUserSubscriptions, TradingUser
from .serializers import UserProfileSerializer
from django.db.models import QuerySet


class UserProfileViewSet(
    ActionPermissionMixin,
    GenericViewSet,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    lookup_field = "pk"
    serializer_class = UserProfileSerializer
    permission_classes_by_action = {"retrieve": (IsOwnerOrAdmin,), "update": (IsAdmin,)}

    def get_queryset(self) -> QuerySet:
        return TradingUser.objects.filter(pk=self.kwargs.get("pk"))


class SubscribeOnPromotionListViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = PromotionListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self) -> QuerySet:
        user = TradingUser.objects.prefetch_related("subscription").get(
            id=self.request.user.id
        )
        promotion_ids = [i.promotion_id for i in user.subscriptions.all()]
        return Promotion.objects.filter(id__in=promotion_ids)

    def create(self, request: Request, *args: tuple, **kwargs: dict) -> response.Response:
        try:
            PromotionUserSubscriptions.objects.get(
                user=request.user, promotion_id=request.data.get("pk")
            )
        except PromotionUserSubscriptions.DoesNotExist:
            PromotionUserSubscriptions.objects.create(
                user=request.user, promotion_id=request.data.get("pk")
            )
            return response.Response(
                "You've been subscribed on promotion", status=status.HTTP_200_OK
            )
        return response.Response(
            "You've been already subscribed on this promotion",
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )

    def delete(self, request: Request) -> response.Response:
        try:
            promotion_user_subscriptions_obj = PromotionUserSubscriptions.objects.get(
                user=request.user, promotion_id=request.data.get("pk")
            )
            promotion_user_subscriptions_obj.delete()
        except PromotionUserSubscriptions.DoesNotExist:
            return response.Response(
                "You've not been subscribed on this promotion",
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
        return response.Response(
            "You've been unsubscribed from this promotion", status=status.HTTP_200_OK
        )
