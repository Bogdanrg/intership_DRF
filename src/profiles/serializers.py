from rest_framework import serializers

from .models import TradingUser


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    avatar = serializers.CharField(read_only=True)
    login = serializers.CharField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    role = serializers.CharField(read_only=True)
    subscription = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)

    class Meta:
        model = TradingUser
        exclude = (
            "password",
            "last_login",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )
