from rest_framework import serializers

from .models import AutoOrder


class CreateAutoOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = AutoOrder
        exclude = ("user",)


class AutoOrderSerializer(serializers.ModelSerializer):
    promotion = serializers.ReadOnlyField(source='promotion.name')
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = AutoOrder
        fields = '__all__'


class AutoOrderListSerializer(serializers.ModelSerializer):
    promotion = serializers.ReadOnlyField(source='promotion.name')

    class Meta:
        model = AutoOrder
        exclude = ('user',)
