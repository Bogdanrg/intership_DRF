from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        if bool(request.user and request.user.is_authenticated):
            return bool(request.user.role == "admin")
        return False


class IsAdminOrAnalyst(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        if bool(request.user and request.user.is_authenticated):
            return bool(request.user.role == "admin" or request.user.role == "analyst")


class IsOwnerOrAdminOrAnalyst(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj) -> bool:
        return bool(
            (obj.user == request.user)
            or (request.user.role == "admin")
            or (request.user.role == "analyst")
        )


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj) -> bool:
        return bool(obj.user == request.user)


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj) -> bool:
        return bool((obj == request.user) or (request.user.role == "admin"))
