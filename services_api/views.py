from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, filters, mixins
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
# from .permissions import UpdateOwnProfile
from rest_framework.viewsets import GenericViewSet

from users_api import permissions
from .custom_permissions import IsServiceProvider
from .serializers import ServiceSerializer, RequestSerializer
from .models import Service, RequestService
from users_api import models


class MakeService(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        user = models.UserProfile.objects.get(id=self.request.user.id)
        serializer.save(service_provider_id=user, service_provider_name=user.name)


class MakeServiceRequest(viewsets.ModelViewSet):
    serializer_class = RequestSerializer
    queryset = RequestService.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        """Create method for user profile"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        status_header = {
            'status': status.HTTP_201_CREATED,
            'message': "User request created successfully.",
            'data': serializer.data
        }
        return Response(status_header)


class ListOfRequestsToProvider(viewsets.ModelViewSet):
    pass


class ListServices(viewsets.ModelViewSet):
    """ViewSet for retrieving services and making a request"""
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class CustomerRequestList(viewsets.ModelViewSet):
    pass
