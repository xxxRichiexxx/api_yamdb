from rest_framework import permissions


class AdminUserModelPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_superuser
                or view.action in ('retrieve', 'update', 'partial_update')
                or request.user.is_authenticated
                and request.user.role == 'admin')

    def has_object_permission(self, request, view, obj):
        return (request.user == obj
                or request.user.is_superuser
                or request.user.is_authenticated
                and request.user.role == 'admin')


class IsAdminOrSuperUserOrReadOnly(permissions.BasePermission):
    message = (
        'Пользователь не является администратором '
        'или супер-пользователем!'
    )

    def has_permission(self, request, view):
        return ((request.user.is_authenticated and request.user.role == 'admin'
                or request.user.is_superuser)
                or request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return ((request.user.is_authenticated and request.user.role == 'admin'
                or request.user.is_superuser)
                or request.method in permissions.SAFE_METHODS)
