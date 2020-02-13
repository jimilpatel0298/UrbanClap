from rest_framework import serializers
from .models import Service, RequestService


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


class RequestSerializer(serializers.ModelSerializer):
    """Create a new request"""
    provider_name = serializers.SerializerMethodField('get_service_provider_name')
    service_name = serializers.SerializerMethodField('get_services_name')

    class Meta:
        model = RequestService
        fields = ('consumer', 'provider_name', 'service_id', 'service_name', 'request_desc',
                  'status', 'comments')
        extra_kwargs = {
            'consumer': {
                'read_only': True
            },
            'service_name': {
                'read_only': True
            },
            'provider_name': {
                'read_only': True
            },
            'status': {
                'read_only': True
            },
            'status': {
                'read_only': True
            },
            'comments': {
                'read_only': True
            }
        }

    def get_service_provider_name(self, data):
        return data.service_id.service_provider.name

    def get_services_name(self, data):
        return data.service_id.service_name

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('author','content')

        extra_kwargs = {
            'author': {
                'read_only': True
            }
        }