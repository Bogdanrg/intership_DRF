from rest_framework import serializers
from .models import PortfolioUserPromotion


class PortfolioSerializer(serializers.ModelSerializer):
    promotion = serializers.ReadOnlyField(source='promotion.name')

    class Meta:
        model = PortfolioUserPromotion
        fields = '__all__'
