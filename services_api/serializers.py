from rest_framework import serializers
from .models import Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('service_name', 'service_desc', 'service_provider')
        extra_kwargs = {
            'service_name': {
                'read_only': True,
            },
            'service_provider': {
                'read_only': True
            }

        }
