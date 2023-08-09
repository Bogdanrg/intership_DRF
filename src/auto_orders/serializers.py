from rest_framework import serializers

from .models import AutoOrder


class CreateAutoOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoOrder
        exclude = ("user",)


class AutoOrderSerializer(serializers.ModelSerializer):
    promotion = serializers.ReadOnlyField(source="promotion.name")
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = AutoOrder
        fields = (
            "id",
            "promotion",
            "user",
            "quantity",
            "status",
            "total_sum",
            "action",
            "closed_at",
            "direction",
        )


class AutoOrderListSerializer(serializers.ModelSerializer):
    promotion = serializers.ReadOnlyField(source="promotion.name")

    class Meta:
        model = AutoOrder
        exclude = ("user",)
