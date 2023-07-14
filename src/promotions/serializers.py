from rest_framework import serializers

from .models import Promotion


class PromotionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ("id", "avatar", "name", "price")


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = "__all__"
