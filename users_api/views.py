"""views for users_api"""
from rest_framework import viewsets, status
from rest_framework.response import Response

from users_api import models, serializers


class UserProfileViewSet(viewsets.ModelViewSet):
    """User profile view"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)