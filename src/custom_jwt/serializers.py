from rest_framework import serializers
from src.profiles.models import TradingUser


class UserCredentialsSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class JWTPairSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=False)
    refresh_token = serializers.CharField()


class RegistrationUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = TradingUser
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        new_user = TradingUser.objects.create_user(**validated_data)
        new_user.is_active = False
        new_user.save()
        return new_user


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    old_password = serializers.CharField()
