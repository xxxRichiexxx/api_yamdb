from rest_framework import permissions


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin)

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and request.user.is_admin)


class ForMePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and view.action in ('retrieve',
                                    'update',
                                    'partial_update',
                                    'destroy'))

    def has_object_permission(self, request, view, obj):
        return view.kwargs['username'] == 'me'


class ReadOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS


class CreateAndUpdatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.user.is_moderator
                or obj.author == request.user)
