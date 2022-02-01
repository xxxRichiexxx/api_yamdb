from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    message = 'Пользователь не является администратором!'

    def has_object_permission(self, request, view, obj):
        return (request.user.is_staff
                or request.method in permissions.SAFE_METHODS)
