from rest_framework import serializers


class UserCredentialsSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class JWTPairSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=False)
    refresh_token = serializers.CharField()
