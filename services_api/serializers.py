from rest_framework import serializers
from .models import Service, RequestService, Comment


class ServiceSerializer(serializers.ModelSerializer):
    """Create a new service"""
    service_provider_name = serializers.SerializerMethodField('get_provider_name')

    class Meta:
        model = Service
        fields = ('id', 'service_name', 'service_desc', 'service_provider_id', 'service_provider_name')
        extra_kwargs = {
            'id': {'read_only': True},
            'service_provider_id': {'read_only': True},
            'service_provider_name': {'read_only': True}
        }

    def get_provider_name(self, data):
        return data.service_provider.name


class CommentSerializer(serializers.ModelSerializer):
    """Create a new comment"""
    author_name = serializers.SerializerMethodField('get_authors_name')

    class Meta:
        model = Comment
        fields = ('id', 'request', 'author', 'content', 'author_name')
        extra_kwargs = {
            'author': {
                'read_only': True
            },
            'author_name': {
                'read_only': True
            }
        }

    def get_authors_name(self, data):
        return data.author.name


class RequestSerializer(serializers.ModelSerializer):
    """Create a new request"""
    provider_name = serializers.SerializerMethodField('get_service_provider_name')
    service_name = serializers.SerializerMethodField('get_services_name')
    # commentslist = serializers.SerializerMethodField('get_commentslists')

    class Meta:
        model = RequestService

        fields = ('id', 'consumer', 'provider_name', 'service_id', 'service_name', 'request_desc',
                  'status', 'comments')

        extra_kwargs = {
            'id': {'read_only': True},
            'consumer': {
                'read_only': True
            },
            'service_name': {
                'read_only': True
            },
            'provider_name': {
                'read_only': True
            },
            'comments': {
                'read_only': True
            },
        }

    def get_service_provider_name(self, data):
        return data.service_id.service_provider.name

    def get_services_name(self, data):
        return data.service_id.service_name
