"""admin for services_api module"""

from django.contrib import admin
from services_api import models

admin.site.register(models.Service)
admin.site.register(models.RequestService)
