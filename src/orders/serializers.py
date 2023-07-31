from rest_framework import serializers
from .models import Order


class OrderListSerializer(serializers.ModelSerializer):
    promotion = serializers.ReadOnlyField(source='promotion.name')

    class Meta:
        model = Order
        exclude = ('user',)


class OrderSerializer(serializers.ModelSerializer):
    promotion = serializers.ReadOnlyField(source='promotion.name')
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Order
        fields = ("id", "promotion", "user", "status", "total_sum", "action")


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ('user',)
