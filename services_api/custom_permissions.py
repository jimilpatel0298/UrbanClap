from rest_framework.permissions import BasePermission


class IsServiceProvider(BasePermission):
    """
    Allows access only to Service Provider.
    """

    def has_permission(self, request, view):
        if request.user.user_type == 'Service Provider':
            return True


class IsConsumer(BasePermission):
    """
    Allows access only to Consumer.
    """

    def has_permission(self, request, view):
        if request.user.user_type == 'Consumer':
            return True

class SeeOwnServices(BasePermission):
    """Allow user to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile"""
        if request.method in BasePermission.SAFE_METHODS:
            return obj.id == request.user.id