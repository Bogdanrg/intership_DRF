from rest_framework import permissions


class ActionPermissionMixin:
    permission_classes_by_action = None

    def get_permissions(self):
        try:
            return [permission() for permission in
                    self.permission_classes_by_action[self.action]]

        except Exception:
            return [permission() for permission in self.permission_classes]


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        if bool(request.user and request.user.is_authenticated):
            return bool(request.user.role == 'admin')
        return False


class IsAdminOrAnalyst(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        if bool(request.user and request.user.is_authenticated):
            return bool(request.user.role == 'admin' or request.user.role == 'analyst')


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return bool((obj.user == request.user) or (request.user.role == 'admin'))
