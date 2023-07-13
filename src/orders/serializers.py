from rest_framework import serializers
from .models import Order


class OrderListSerializer(serializers.ModelSerializer):
    promotion = serializers.ReadOnlyField(source='promotion.name')

    class Meta:
        model = Order
        exclude = ('user', )


class OrderSerializer(serializers.ModelSerializer):
    promotion = serializers.ReadOnlyField(source='promotion.name')

    class Meta:
        model = Order
        fields = '__all__'
