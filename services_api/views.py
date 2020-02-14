from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, filters, mixins
from django.core import serializers
from rest_framework import status, viewsets, mixins, generics
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from .custom_permissions import IsServiceProvider, IsConsumer
from .serializers import ServiceSerializer, RequestSerializer, CommentSerializer
from .models import Service, RequestService, Comment
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

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()
        print(instance.request.filter(status='accepted').count())
        if instance.request.filter(status='accepted').count() == 0:
            self.perform_destroy(instance)
            status_header = {
                'status': status.HTTP_200_OK,
                'message': "Service Deleted Successfully.",
            }
            return Response(status_header)
        else:
            status_header = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': "The service is currently accepeted. Hence cannot be deleted.",
            }
            return Response(status_header)



    def perform_destroy(self, instance):
        instance.delete()


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
    """List of requests to service provider"""
    serializer_class = RequestSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsServiceProvider)



    # jimil
    # def get_queryset(self):
    #     data = Service.objects.filter(service_provider=self.request.user.id)
    #     print(data)
    #     list = []
    #     for d in data:
    #         data1 = d.request.all()
    #         data2 = data1.values()
    #         list.append(data2)
    #     print(list)
    #     return list

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)




    # maitri
    # def get_queryset(self):
    #     service_obj = self.request.user.services.filter(service_provider=self.request.user)
    #     x=[]
    #     # print(service_obj)
    #     for obj in service_obj:
    #         print(obj.id)
    #         # print(obj.request.all())
    #         # x.append(obj.request.all())
    #         print(RequestService.objects.get(service_id = obj.id))
    #     return x
    #
    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     status_header = {
    #         'status': status.HTTP_200_OK,
    #         'message': "List of requests received successfully.",
    #         'data': serializer.data
    #     }
    #     return Response(status_header)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if request.data['status'].lower() not in ['accepted', 'rejected', 'pending', 'completed']:
            return Response({'status': status.HTTP_400_BAD_REQUEST,
            'message': "Status can be only 'accepted', 'rejected', 'pending' or 'completed'."})

        if instance.status.lower() == 'accepted' and request.data['status'].lower() == 'rejected':
            return Response({'status': status.HTTP_400_BAD_REQUEST,
            'message': "You cannot change status now."})
        serializer = self.get_serializer(instance, data={'status': request.data['status'].lower()}, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        status_header = {
            'status': status.HTTP_200_OK,
            'message': "Service request status changed successfully.",
            'data': serializer.data
        }
        return Response(status_header)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


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
            'status': status.HTTP_200_OK,
            'message': "List of services received successfully.",
            'data': serializer.data
        }
        return Response(status_header)


class CreateComment(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                     GenericViewSet):  # Final
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):

        """Make comment on request"""

        obj = RequestService.objects.get(id=self.request.data['request'])
        if obj.status == 'pending':
            status_header = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': "You are not allow to comment, status is pending!.",
            }
            return Response(status_header)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(author=self.request.user)
            status_header = {
                'status': status.HTTP_201_CREATED,
                'message': "User comment created successfully.",
                'data': serializer.data
            }
            return Response(status_header)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ViewComments(APIView):

    serializer_class = CommentSerializer

    def get(self, request, pk):
        comments = Comment.objects.filter(request=pk)
        data = CommentSerializer(comments, many=True).data
        return Response(data)