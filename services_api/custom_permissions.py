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
