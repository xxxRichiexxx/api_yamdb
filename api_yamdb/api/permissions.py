from rest_framework import permissions


class IsAdminOrSuperUserOrReadOnly(permissions.BasePermission):
    message = (
        'Пользователь не является администратором '
        'или супер-пользователем!'
    )

    def has_object_permission(self, request, view, obj):
        return ((request.user.is_staff
                or request.user.is_superuser)
                or request.method in permissions.SAFE_METHODS)
