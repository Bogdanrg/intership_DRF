from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .models import Promotion
from .serializers import PromotionSerializer


class ListCreatePromotionAPIView(
    mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet
):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
