from rest_framework import permissions


class AdminUserModelPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.role == 'admin' or
                request.user.is_superuser or
                view.action in ('retrieve', 'update', 'partial_update'))

    def has_object_permission(self, request, view, obj):
        return (request.user.role == 'admin' or
                request.user.is_superuser or
                request.user == obj)
