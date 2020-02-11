from rest_framework import serializers
from .models import Service,RequestService



class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id','service_name', 'service_desc', 'service_provider')
        extra_kwargs = {
            'id':{'read_only': True}
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
        # fields = ('')
