from django.db.models import Model
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.user and request.user.is_authenticated:
            return bool(request.user.role == "admin")
        return False


class IsAdminOrAnalyst(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.user and request.user.is_authenticated:
            return bool(request.user.role == "admin" or request.user.role == "analyst")
        return False


class IsOwnerOrAdminOrAnalyst(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(
        self, request: Request, view: APIView, obj: Model
    ) -> bool:
        return bool(
            (obj.user == request.user)
            or (request.user.role == "admin")
            or (request.user.role == "analyst")
        )


class IsOwner(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(
        self, request: Request, view: APIView, obj: Model
    ) -> bool:
        return bool(obj.user == request.user)


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(
        self, request: Request, view: APIView, obj: Model
    ) -> bool:
        return bool((obj == request.user) or (request.user.role == "admin"))
