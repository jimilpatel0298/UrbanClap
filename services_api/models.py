from django.db import models
from djongo import models as m
from users_api.models import UserProfile
from django.conf import settings


# Create your models here.
class Service(models.Model):
    """ Database model for Services """
    service_name = models.CharField(max_length=255)
    service_desc = models.CharField(max_length=255)
    service_provider_name = models.CharField(max_length=255)
    service_provider_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    no_of_requests = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    author = models.CharField(max_length=255)
    content = models.CharField(max_length=255)


class RequestService(models.Model):
    """ Database model for requested services by customer. """
    consumer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requestmade')
    provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requestrecieved')
    service_id = models.ForeignKey('Service', on_delete=models.CASCADE, null=False)
    request_desc = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    request_updated_at = models.DateTimeField(auto_now=True)
    comments = m.ArrayField(model_container=Comment)
