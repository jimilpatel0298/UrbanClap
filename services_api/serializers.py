from rest_framework import serializers
from .models import Service, RequestService


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'service_name', 'service_desc', 'service_provider')
        extra_kwargs = {
            'id': {'read_only': True}
            #     'service_name': {
            #         'read_only': True,
            #     },
            #     'service_provider': {
            #         'read_only': True
            #     }
            #
        }


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestService
        fields = ('customer', 'provider', 'service_id', 'request_desc', 'status', 'comments')
        extra_kwargs = {
            # 'id': {'read_only': True}
            'customer': {
                'read_only': True
            },
            'provider': {
                'read_only': True
            },
            'service_id': {
                'read_only': True
            },
            'request_desc': {
                'read_only': True
            },
            'status': {
                'read_only': True
            },
            'comments': {
                'read_only': True
            }
        }
