from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, filters, mixins
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from .custom_permissions import IsServiceProvider, IsConsumer
from .serializers import ServiceSerializer, RequestSerializer, CommentSerializer
from .models import Service, RequestService
from users_api import models


class MakeService(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsServiceProvider)

    def get_queryset(self):
        return Service.objects.filter(service_provider=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = models.UserProfile.objects.get(id=self.request.user.id)
        serializer.save(service_provider=user)
        status_header = {
            'status': status.HTTP_201_CREATED,
            'message': "Provider service created successfully.",
            'data': serializer.data
        }
        return Response(status_header)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        status_header = {
            'status': status.HTTP_201_CREATED,
            'message': "List of provider services received successfully.",
            'data': serializer.data
        }
        return Response(status_header)


class MakeServiceRequest(viewsets.ModelViewSet):
    serializer_class = RequestSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsConsumer)

    def create(self, request, *args, **kwargs):
        """Create method for user profile"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = models.UserProfile.objects.get(id=self.request.user.id)
        service = Service.objects.get(id=self.request.POST.get('service_id'))
        serializer.save(consumer=user, service_id=service)
        status_header = {
            'status': status.HTTP_201_CREATED,
            'message': "User request created successfully.",
            'data': serializer.data
        }
        return Response(status_header)

    def get_queryset(self):
        return RequestService.objects.filter(consumer=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        status_header = {
            'status': status.HTTP_201_CREATED,
            'message': "List of user requests received successfully.",
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
    permission_classes = (IsAuthenticated, IsConsumer)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        status_header = {
            'status': status.HTTP_201_CREATED,
            'message': "List of services received successfully.",
            'data': serializer.data
        }
        return Response(status_header)


class CreateComment(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = CommentSerializer
    queryset = Service.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
