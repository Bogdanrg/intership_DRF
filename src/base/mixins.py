from typing import Dict

from rest_framework.serializers import Serializer


class ActionPermissionMixin:
    permission_classes_by_action: Dict[str, tuple]
    action: str
    permission_classes: list

    def get_permissions(self) -> list:
        try:
            return [
                permission()
                for permission in self.permission_classes_by_action[self.action]
            ]

        except Exception:
            return [permission() for permission in self.permission_classes]


class ActionSerializerMixin:
    serializer_class: Serializer
    action: str
    serializer_classes_by_action: Dict[str, Serializer]

    def get_serializer_class(self) -> Serializer:
        try:
            return self.serializer_classes_by_action[self.action]

        except Exception:
            return self.serializer_class
