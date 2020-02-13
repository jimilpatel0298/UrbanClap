from rest_framework import serializers
from .models import Service, RequestService


class ServiceSerializer(serializers.ModelSerializer):
    """Create a new service"""

    class Meta:
        model = Service
        fields = ('id', 'service_name', 'service_desc', 'service_provider_id', 'service_provider_name')
        extra_kwargs = {
            'id': {'read_only': True},
            'service_provider_id': {'read_only': True},
            'service_provider_name': {'read_only': True}
        }


class RequestSerializer(serializers.ModelSerializer):
    """Create a new request"""

    class Meta:
        model = RequestService
        fields = ('consumer', 'provider', 'service_id', 'request_desc', 'status', 'comments')
        extra_kwargs = {
            'consumer': {
                'read_only': True
            },
            'provider': {
                'read_only': True
            },
            'status': {
                'read_only': True
            },
            # 'comments': {
            #     'read_only': True
            # }
        }
