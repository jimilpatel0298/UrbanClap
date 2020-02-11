from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status,viewsets,filters
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
# from .permissions import UpdateOwnProfile
from .serializers import ServiceSerializer
from .models import Service,RequestService


class ListOfServices(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email',)

class ListOfRequestsToProvider(viewsets.ModelViewSet):
    pass


class MakeServiceRequest(viewsets.ModelViewSet):
    pass


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