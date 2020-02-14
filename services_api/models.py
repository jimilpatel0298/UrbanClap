from django.db import models
from django.db.models import ForeignKey
from djongo import models as m
from users_api.models import UserProfile
from django.conf import settings


class Service(models.Model):
    """ Database model for Services """
    service_name = models.CharField(max_length=255)
    service_desc = models.CharField(max_length=255)
    service_provider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , related_name='services')
    no_of_requests = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    """ Database model to add comments. """
    request = models.ForeignKey('RequestService',on_delete=models.CASCADE, related_name= 'comments',null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , related_name='comments')
    content = models.CharField(max_length=255)


class RequestService(models.Model):
    """ Database model for requested services by customer. """
    consumer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requestmade')
    service_id = models.ForeignKey('Service', on_delete=models.CASCADE, null=False , related_name='request')
    request_desc = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    request_updated_at = models.DateTimeField(auto_now=True)

