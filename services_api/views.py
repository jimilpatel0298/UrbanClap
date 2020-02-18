"""Provider and Consumer related views"""
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from .custom_permissions import IsServiceProvider, IsConsumer
from .serializers import ServiceSerializer, RequestSerializer, CommentSerializer
from .models import Service, RequestService, Comment
from users_api import models


class MakeService(viewsets.ModelViewSet):
    """Provider service view"""
    serializer_class = ServiceSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsServiceProvider)

    def get_queryset(self):
        return Service.objects.filter(service_provider=self.request.user)

    def create(self, request, *args, **kwargs):
        """create service method for provider"""
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
        """List method to view all services profiles"""
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

    def retrieve(self, request, *args, **kwargs):
        """Method to retrive particular service."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        status_header = {
            'status': status.HTTP_201_CREATED,
            'message': "Services received successfully.",
            'data': serializer.data
        }
        return Response(status_header)

    def update(self, request, *args, **kwargs):
        """Method to update particular service."""
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
            'status': status.HTTP_201_CREATED,
            'message': "Services Updated successfully.",
            'data': serializer.data
        }
        return Response(status_header)

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """Method to delete particular service."""
        instance = self.get_object()
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
    """User request view"""
    serializer_class = RequestSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsConsumer)

    def create(self, request, *args, **kwargs):
        """Create method to request services for consumer"""
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
        """List method to view all request to consumer"""
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        sort_field = self.request.query_params.get('sort_by', None)
        # Enter url like '{{base_url}}/api/consumer/requests?sort_by=status/service_id or -status/-service_id'

        if sort_field is not None:
            if (sort_field == 'status') or (sort_field == 'service_id') or (sort_field == '-status') or (
                    sort_field == '-service_id'):
                serializer = self.get_serializer(queryset.order_by(sort_field), many=True)
            else:
                status_header = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': "Bad sorting request.",
                }
                return Response(status_header)
        else:
            serializer = self.get_serializer(queryset, many=True)

        status_header = {
            'status': status.HTTP_201_CREATED,
            'message': "List of user requests received successfully.",
            'data': serializer.data
        }
        return Response(status_header)

    def retrieve(self, request, *args, **kwargs):
        """Method to retrive particular request."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        status_header = {
            'status': status.HTTP_201_CREATED,
            'message': "User request received successfully.",
            'data': serializer.data
        }
        return Response(status_header)

    def update(self, request, *args, **kwargs):
        """Method to update particular request."""
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
            'status': status.HTTP_201_CREATED,
            'message': "User request updated successfully.",
            'data': serializer.data
        }
        return Response(status_header)

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """Method to delete particular request."""
        instance = self.get_object()
        if instance.status != "accepted":
            self.perform_destroy(instance)
            status_header = {
                'status': status.HTTP_200_OK,
                'message': "Request Deleted Successfully.",
            }
            return Response(status_header)
        else:
            status_header = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': "The request is currently accepeted. Hence cannot be deleted.",
            }
            return Response(status_header)

        # return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class ListOfRequestsToProvider(viewsets.ModelViewSet):
    """List of requests to service provider"""
    serializer_class = RequestSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsServiceProvider)

    def get_queryset(self):
        service_obj = self.request.user.services.filter(service_provider=self.request.user)
        request_to_user = []
        for obj in service_obj:
            if len(obj.request.all()) != 0:
                for i in obj.request.all():
                    request_to_user.append(i)
        return request_to_user

    def list(self, request, *args, **kwargs):
        """List method to view all request to provider"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        status_header = {
            'status': status.HTTP_200_OK,
            'message': "List of requests received successfully.",
            'data': serializer.data
        }
        return Response(status_header)

    def retrieve(self, request, *args, **kwargs):
        """Method to retrive particular request."""
        instance = RequestService.objects.get(id=self.kwargs.get('pk'))
        serializer = self.get_serializer(instance)
        status_header = {
            'status': status.HTTP_200_OK,
            'message': "Requests received successfully.",
            'data': serializer.data
        }
        return Response(status_header)

    def update(self, request, *args, **kwargs):
        """Method to update particular request."""
        partial = kwargs.pop('partial', False)
        instance = RequestService.objects.get(id=self.kwargs.get('pk'))
        if request.data['status'].lower() not in ['accepted', 'rejected', 'pending', 'completed']:
            return Response(
                {'status': status.HTTP_400_BAD_REQUEST,
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


class ListServices(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """ViewSet for retrieving services"""
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsConsumer)

    def list(self, request, *args, **kwargs):
        """List method to view all services to consumer"""
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
                    GenericViewSet):
    """Create comment view"""
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
        """Method to retrive particular comment."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        status_header = {
            'status': status.HTTP_201_CREATED,
            'message': "Comment recieved successfully.",
            'data': serializer.data
        }
        return Response(status_header)


class ViewComments(APIView):
    """View for list of comments per request"""
    serializer_class = CommentSerializer

    def get(self, request, pk):
        """Method to get comments on get method."""
        comments = Comment.objects.filter(request=pk)
        data = CommentSerializer(comments, many=True).data
        status_header = {
            'status': status.HTTP_201_CREATED,
            'message': "Comments recieved successfully.",
            'data': data,
        }
        return Response(status_header)
