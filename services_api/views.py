from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status, viewsets, filters, mixins
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from .custom_permissions import IsServiceProvider, IsConsumer
from .serializers import ServiceSerializer, RequestSerializer
from .models import Service, RequestService


class MakeService(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, IsServiceProvider, ]
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('service_name', 'service_provider',)


class ListOfServices(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, IsConsumer, ]
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()


class ListOfRequestsToProvider(viewsets.ModelViewSet):
    pass


class MakeServiceRequest(viewsets.ModelViewSet):
    serializer_class = RequestSerializer
    # queryset = RequestService.objects.all()


class CustomerRequestList(viewsets.ModelViewSet):
    pass

