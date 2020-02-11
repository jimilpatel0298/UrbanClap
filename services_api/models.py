from django.db import models
from djongo import models as m


# Create your models here.
class Service(models.Model):
    """ Database model for Services """
    service_name = models.CharField(max_length=255)
    service_desc = models.CharField(max_length=255)
    service_provider = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    no_of_requests = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    author = models.CharField(max_length=255)
    content = models.CharField(max_length=255)


class RequestService(models.Model):
    """ Database model for requested services by customer. """
    customer = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    provider = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    service_id = models.ForeignKey('Service', on_delete=models.CASCADE, null=False)
    request_desc = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    request_updated_at = models.DateTimeField(auto_now=True)
    comments = m.ArrayField(model_container=Comment)


