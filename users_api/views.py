"""views for users_api"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

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
        print(serializer.data)

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
            "data": serializer.data
        }
        return Response(status_header)

