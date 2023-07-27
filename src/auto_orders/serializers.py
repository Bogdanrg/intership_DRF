from rest_framework import serializers

from .models import AutoOrder


class CreateAutoOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoOrder
        exclude = ("user",)
