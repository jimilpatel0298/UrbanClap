from rest_framework.permissions import BasePermission


class IsServiceProvider(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        print("self.request.user.user_type : ", self.request.user.user_type)
        return True