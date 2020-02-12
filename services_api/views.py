from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status, viewsets, filters, mixins
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
# from .permissions import UpdateOwnProfile
from rest_framework.viewsets import GenericViewSet

from .custom_permissions import IsServiceProvider
from .serializers import ServiceSerializer, RequestSerializer
from .models import Service, RequestService


class MakeService(viewsets.ModelViewSet):
    permission_classes = [IsServiceProvider]
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()

    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('name','email',)


class ListOfServices(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    # def list(self,request):
    #     q = Service.objects.all()
    #     serializer_class = ServiceSerializer(q, many=True)
    #     return Response(data=serializer_class.data)
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('name','email',)


class ListOfRequestsToProvider(viewsets.ModelViewSet):
    pass


class MakeServiceRequest(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = RequestSerializer
    queryset = Service.objects.all()

    # def perform_create(self, serializer):
        # serializer.save(customer = self.request.user, provider = self. )


class CustomerRequestList(viewsets.ModelViewSet):
    pass

# class UserProfileViewSet(viewsets.ModelViewSet):
#     serializer_class = UserProfileSerializer
#     queryset = UserProfile.objects.all()
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (UpdateOwnProfile,)
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ('name','email',)
#
#
# class UserLoginApiView(ObtainAuthToken):
#     renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
