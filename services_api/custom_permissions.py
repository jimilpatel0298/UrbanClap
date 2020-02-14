from rest_framework.permissions import BasePermission, SAFE_METHODS


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



class StatusCheck(BasePermission):
    """
    Allows access to comment if request status is not pending.
    """
    def has_permission(self, request, view):
        """Check user is trying to edit their own profile"""
        print("heyy", obj)
        return False
        # if request.method in SAFE_METHODS:
        #     return True
        # return obj.id == request.user.id
