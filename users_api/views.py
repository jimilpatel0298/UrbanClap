"""views for users_api"""
from rest_framework import viewsets, status, mixins
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from users_api import models, serializers, permissions


class UserProfileViewSet(viewsets.ModelViewSet):
    """User profile view"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)

    def create(self, request, *args, **kwargs):
        """Create method for user profile"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        status_header = {
            'status': status.HTTP_201_CREATED,
            'message': "User profile created successfully.",
            'data': serializer.data
        }
        return Response(status_header)

    def list(self, request, *args, **kwargs):
        """List method to view all user profiles"""
        queryset = models.UserProfile.objects.all()
        serializer = self.get_serializer(queryset, many=True)

        if serializer.data:
            status_header = {
                'status': status.HTTP_200_OK,
                'message': "List of user profiles received successfully.",
                'data': serializer.data
            }
        else:
            status_header = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': "No users found",
                "data": {}
            }
        return Response(status_header)


class UserLoginViewSet(ObtainAuthToken):
    """User Login view"""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        status_header = {
            "status": status.HTTP_200_OK,
            "message": "User Logged In Successfully.",
            "token": token.key,
            "data": {"email": serializer.data['username']}
        }
        return Response(status_header)


class ChangePasswordView(viewsets.ModelViewSet):
    serializer_class = serializers.ChangePasswordSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)

    def update(self, request, *args, **kwargs):
        if request.data['old_password'] == request.data['new_password']:
            response = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'New Password should be different from Old Password',
            }
            return Response(response)

        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': status.HTTP_200_OK,
                'message': 'Password updated successfully',
            }
            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateView(viewsets.ModelViewSet):
    """View for updating user profile"""
    serializer_class = serializers.UserProfileUpdateSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, permissions.UpdateOwnProfile,)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        status_header = {
            'status': status.HTTP_200_OK,
            'message': "User data changed successfully.",
            "data": serializer.data
        }
        return Response(status_header)


class UserLoginViewSet(ObtainAuthToken):
    """User Login view"""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        status_header = {
            "status": status.HTTP_200_OK,
            "message": "User Logged In Successfully.",
            "token": token.key,
            "data": serializer.data
        }
        return Response(status_header)


class Logout(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

