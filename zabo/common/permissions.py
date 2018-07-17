from rest_framework import permissions
from operator import eq

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner
        return obj.owner == request.user


class IsOwnerOrIsAuthenticatdThenCreateOnlyOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    message = "It's not permissioned"

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        UPDATE_METHODS = ('PUT', 'PATCH')

        if request.method in permissions.SAFE_METHODS:
            return True
        elif eq(request.method, 'POST') or eq(request.method, 'DELETE'):
            return  request.user and request.user.is_authenticated
        elif request.method in UPDATE_METHODS:
            return obj.author == request.user

        # Other method does not permissioned.
        return False


class IsAuthenticated(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True
        return super(IsAuthenticated, self).has_permission(request, view)
