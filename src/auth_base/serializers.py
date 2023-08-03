from rest_framework import serializers


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class JWTPairSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=False)
    refresh_token = serializers.CharField()


class RegistrationUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    repeat_password = serializers.CharField()
    email = serializers.CharField()

    def validate(self, data) -> dict:
        if not data["password"] == data["repeat_password"]:
            raise serializers.ValidationError("Password missmatch")
        return data


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    old_password = serializers.CharField()


class ResetPasswordSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()


class ConfirmResetPasswordSerializer(serializers.Serializer):
    username = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField()
